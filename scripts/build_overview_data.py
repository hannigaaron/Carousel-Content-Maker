import os, re, json
ROOT="/home/user/Carousel-Content-Maker"
S=os.path.dirname(os.path.abspath(__file__))

def quotes(s):
    out=[]
    for ch in s:
        if ch=='"':
            prev=out[-1] if out else " "
            out.append("\u201c" if (prev.isalnum() or prev in ".,!?)\u201c\u2019") else "\u201e")
        else:
            out.append(ch)
    return "".join(out)

def unwrap(cap):
    paras=[p for p in cap.strip().split("\n\n")]
    out=[]
    for i,p in enumerate(paras):
        if i==len(paras)-1:          # CTA-Block: Zeilenumbrüche sind gewollt
            out.append(p.strip())
        else:
            out.append(" ".join(l.strip() for l in p.split("\n")))
    return "\n\n".join(out)

def parse(week,p):
    t=open(f"{ROOT}/posts/{week}/post-{p}.md").read()
    title=re.search(r"^# (.+)$",t,re.M).group(1).strip()
    thema=re.search(r"^thema: (.+)$",t,re.M).group(1).strip()
    kat=re.search(r"^kategorie: (.+)$",t,re.M).group(1).strip()
    schmerz=re.search(r'^zielgruppen-schmerz: "?(.+?)"?$',t,re.M).group(1).strip()
    warum=re.search(r"## Warum dieses Thema\n\n(.*?)\n\n## ",t,re.S).group(1)
    warum=" ".join(l.strip() for l in warum.strip().split("\n"))
    cap=unwrap(re.search(r"## Caption\n(.*?)\n## Hashtags",t,re.S).group(1))
    offen=re.search(r"## Offene Punkte\n(.*?)$",t,re.S)
    offen=[quotes(" ".join(x.split())) for x in offen.group(1).strip().split("\n\n")] if offen else []
    rows=[]
    for m in re.finditer(r"^\| (\d+) \| `([^`]+)` \| (.+?) \| (.+?) \|$",t,re.M):
        rows.append({"n":int(m.group(1)),"counter":m.group(2),
                     "headline":quotes(m.group(3).strip()),"foto":m.group(4).strip()})
    d=f"{ROOT}/posts/{week}/post-{p}-slides"
    imgs=[f"slides/{week[5:]}-p{p}-{f.split('-')[1].split('.')[0]}.jpg"
          for f in sorted(os.listdir(d)) if f.endswith(".png")]
    return {"nr":p,"title":title,"thema":thema,"kategorie":kat,"schmerz":quotes(schmerz),
            "warum":quotes(warum),"caption":quotes(cap),"offen":offen,"slides":rows,"images":imgs}

data=[]
for week,posts in (("2026-W37",(1,2)),("2026-W35",(1,2,3))):
    data.append({"week":week,"posts":[parse(week,p) for p in posts]})
open(f"{S}/data.json","w").write(json.dumps(data,ensure_ascii=False,indent=1))
# caption.txt im Upload-Ordner mit sauberen Umbrüchen neu schreiben
for wk in data:
    base=f"{ROOT}/FERTIG-ZUM-HOCHLADEN/{wk['week']}"
    for post in wk["posts"]:
        for folder in os.listdir(base):
            if folder.startswith(f"{post['nr']} — "):
                open(f"{base}/{folder}/caption.txt","w").write(post["caption"]+"\n")
print("ok", sum(len(w["posts"]) for w in data), "posts")

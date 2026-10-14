from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def save(name,engine,example,questions,rows,**extra):
    cards=[]
    for line in rows.strip().splitlines():
        cells=[x.strip() for x in line.split('|')]
        assert len(cells)==8,(name,cells)
        cells[0]=int(cells[0]);cells[1]=int(cells[1]);cards.append(cells)
    data={'class':name,'engine':engine,'workedExample':example,'balanceQuestions':questions,'cards':cards,**extra}
    path=ROOT/'data/playtest/class_drafts';path.mkdir(parents=True,exist_ok=True)
    target=path/(name.lower().replace(' ','-')+'.json')
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(name,len(cards),'authored cards')

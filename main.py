import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction


class NettekimExtension(Extension):
    def __init__(self):
        super(NettekimExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()
        script = extension.preferences["script"]

        getir = os.popen("lsof -i").read()
        
        boluk = getir.split("\n")
        baslk = boluk.pop(0).split()
        liste = {}
        
        for j,i in enumerate(boluk):
            col = i.split()
            if len(col) < 3: continue
            col[-2] += col[-1]
            col.remove(col[-1])
        
            liste[str(j)] = {}

            for t,k in enumerate(col):
                liste[str(j)][baslk[t]] = k
        
        
        # Seçili Stil'i bulur. Sorgu satırına yazılan kod, ayarlardaki koddan üstündür.
        selected = extension.preferences["tips"]
        for i in ["t0", "t1", "t2", "t3", "t4", "t5", "t6"] :
            if i in query:
                selected = i
                query = query.replace(i,"").strip()
        
        items = []
        
        if selected == "t0":
            # Aynı dosya isimleri  başlıkta birleştirilmiş, bağlantı adresleri açıklamada 
            o = {}
            for i in liste.keys():
                if liste[i]["COMMAND"] in o:
                    o[liste[i]["COMMAND"]].append(liste[i]["NAME"])
                else:
                    o[liste[i]["COMMAND"]] = [liste[i]["NAME"]]
            
                
            query = query.replace("t0","").strip()
            for i in o.keys():
                if len(query) > 0:
                    if query in i:
                        items.append(ExtensionResultItem(icon='images/icon.png',
                                    name=i,
                                    description="\n".join(o[i]),
                                    on_enter=RunScriptAction(script)))
                else:
                    items.append(ExtensionResultItem(icon='images/icon.png',
                                    name=i,
                                    description="\n".join(o[i]),
                                    on_enter=RunScriptAction(script)))
        else:
            desc_list = ["NAME", "USER", "PID", "TYPE", "NODE", "DEVICE"]
            desc = lambda i: "\n".join([desc_list[u] + " : " + liste[i][desc_list[u]] for u in range(int(selected[1]))])
            for i in liste.keys():
                if len(query) > 0:
                    if query in liste[i]["COMMAND"]:
                        items.append( ExtensionResultItem(icon='images/icon.png',
                                    name=liste[i]["COMMAND"],
                                    description=desc(i),
                                    on_enter=RunScriptAction(script))
                                )
                else:
                    items.append( ExtensionResultItem(icon='images/icon.png',
                                    name=liste[i]["COMMAND"],
                                    description=desc(i),
                                    on_enter=RunScriptAction(script))
                                )

        return RenderResultListAction(items)


if __name__ == '__main__':
    NettekimExtension().run()

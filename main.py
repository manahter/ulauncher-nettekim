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
        
           
        if "t0" in query or extension.preferences["tips"] == "t0":
            items = [
                ExtensionResultItem(icon='images/icon.png',
                                    name=liste[i]["COMMAND"],
                                    description=liste[i]["NAME"],
                                    on_enter=RunScriptAction(script))
                for i in liste.keys()
            ]
        elif "t1" in query or extension.preferences["tips"] == "t1":
            o = {}
            for i in liste.keys():
                if liste[i]["COMMAND"] in o:
                    o[liste[i]["COMMAND"]].append(liste[i]["NAME"])
                else:
                    o[liste[i]["COMMAND"]] = [liste[i]["NAME"]]
            
            items = [
                ExtensionResultItem(icon='images/icon.png',
                                    name=i,
                                    description="\n".join(o[i]),
                                    on_enter=RunScriptAction(script))
                for i in o.keys()
            ]

        return RenderResultListAction(items)


if __name__ == '__main__':
    NettekimExtension().run()

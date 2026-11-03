"""Genera el CSS de colores de los botones de submenú de BOT CC.

Uso:
    python generar_colores_botones.py <export_typebot.json> <salida.json> <salida.css>

- Lee los botones (choice input) del export de Typebot.
- Falla si un ID listado en C o NAV ya no existe, o si hay un botón nuevo sin categoría
  (así se detecta un botón recreado, que cambia de ID).
- Inserta o reemplaza la sección "Botones de los submenús" del Custom CSS del tema,
  antes de la sección de valoración, y escribe el export y el CSS resultantes.

Para agregar un botón: sumar su ID a la lista de color que corresponda (C) o a NAV.
"""
import json,sys
t=json.load(open(sys.argv[1]))
items={it['id']:(g['title'],it.get('content')) for g in t['groups'] for b in g['blocks'] if b['type']=='choice input' for it in b['items']}
C={
'orange':['eln0zqqfypfc8pt5h6z8z0p7','h9bx9mjngojoxh8yoeotjxms','p7mcqzzhwdp7ritivwoj9m01','baje72l19oofs8q52j6r4qdh',
          'ipgcan2zw749vbjm4kiv1lqp','cv0ysexu7elb63avf3m7ia7a','jyu120rve5ydrxuf24irfc86','ykaw5bbl190zwh7wlrlqesjc',
          'ufapaod45kpvez5pkszuew0b','vmvuj13s3op1gg4wgygj9hqt','x7myuxf9v5zl9s1pq4k2zhbs'],
'red':['zlotj22wqma2qmcwz4k0yy4p','az6w6o38t5miepgvy9lom2nt','zyajm1pwpo13t4kmr7bxabzg'],
'yellow':['gp3lhob3wd40zbfv8jpdw4yl','rtzxpz4vf19n6ecm1zp3powe','z9wtndolnsx3sib128dr54v0','e4mpocqwxl5ee54arihj7mot','ekujv3o9e2zif0bdfwa3ko8l'],
'blue':['sihvk5x4bym5shx7k3f6oonh','zo39ct2qsggced0gkp7u5sd5','woh7f757kjt78aq8iaet0vjt','xv0t3q7gqz3zsrhfmc6fak20',
        'z33qr72cd7vm7tkc5chbnlbf','ejpjc9w7gjifeqf8gox3713t','io8sfs4g4wjablx2x9j6g8xa','uxp6vxmdttj2tr6dw6t3wjgg','qe648yjdlecvmebdcz5y5i2f',
        'pqocqy4vsiugsnz2h9e63pts','n0wojycbdvzm697lrmr3lnsh','yjc1fy6pyhyg32ernqax7dox','w74rloc27zzu7td8x4q10oof','svbavrmmbgca2motlmmeddfa',
        'ajeh454vmxbvrhv65lx2imjf','g0mkwnj3294293xfovr07601','icilifaikmqchyle138jac33','amafotrkln0gvrmyo2b1fmqp','qhf8q36erezpabgn402q6vgt'],
'green':['l9ruxxk6zm3g1ojwlq8ab90r','djrmx6ho7ajqzvxlqou5n0ge','tbx1cvz4tn9m89h2c6cfe2iu','vu524vrokf6z07tnp0j2st4u','u67s7jt25hgcnnkpj0igc0em',
         'dbe8w3l6czqigukxypxb2nxc','u17lw4tgw7kh7uw0ggn4re88','xi6sqcriwdhl2n1ue8yg6fg6','n1frrfnhq9d1g3mworgq5ddw','e18o1bnl3t7r68ah45spdlas',
         'uecrbtmfeqvx1q395pyeu4wk'],
'violet':['eqwoacqtxrz94w4rsn5b6bcg','a2jv621wh9yke1ii4san9mo0','o6522vwmmvanlufqtk2s411q','oin4mbbghk4xzxmmimuyz4gj','l9vjbksg9bp9hqyeh06unt3z',
          'lfq4uskz7xjq8nwqea1vfr3x','l4znt81sxr3q520icjuwaxpx','euo7a4xuyfxrcpy88gczkt11','jv07r4jzhmsf9bumzmplktlf','dl0mmgfyzlebo3zpbp0lwsx0','xny5xbqptonrntb1amnyjn61'],
'neutral':['ltkzhdhrcqypr620hjtb3z2h','wngoaxq71q4bxnsl2ut64rhk'],
}
NAV=['jkp2wkhmw2pqj7ff1ofh6nlm','zqdksnr8kir1h2f1uy915oqk','vtpit4a6ghpcuats1xzbdmks','kfqlrrj0lwhgmq66k5u1wh82','h158ls0giv9753q8ior0rmop',
     'v90utysjqnphdrr8l6tvlv3o','f69lsfgc6qkg6v6iano0b4f1','aqtmlmd62hrav57plaqvj61c','ka3fgkuv2kjqoe68qspz0e0p','quwlp72ey51deyyisqyx4vex',
     'ryj9u35auhwe46ssri3kvhnf','wx5j3wjmidxq2lljukfltcyd','f5x0l2utlo8ev4fbe0vq6xl2','zwtaxpacczh61ftwkch9qtyw','igxbpt3laowfvgaea35mmep1',
     'h6waryvub6g9vwhx128g4rxh','zisagniecm62xmvxeoki2vzj','gm1imzcz1eppt7ek3misld0r','piz1hepvxqp9ridbtul4cgxs','eatazeev8duc4ruugrlwky1o',
     'rpn5pqgnygwahtmfqahv4mvk','dmjfd2izh9b0bkvhibvaaylt','qatr10iv8nom0wmmcbohtp37']
allids=[i for v in C.values() for i in v]+NAV
assert len(allids)==len(set(allids)), 'dup'
for i in allids: assert i in items, i
menu=['htrpuji0daqqk5s84z1wm9zj','j5pzbt8oud7dtgzr2xdh5g86','njhsbtl85bit6bds5ying8qe','d1yngatjgld7vyww3w5w25b6','ogtm0kcd0yir77guhfydrtw6','okh285fozedou5roi3vvz1zi','qemktamapbee0hqqqo3vbgtq','rudcv85o0h3hy10pcvl0qgi3','it7cav5lwbfuj061otdlns56','p3jfalj019dc5xwfou6kcs4k','e4hc1ksvgjlt00uvttdgezj7','c5chvsxffub5s3kdbzfrnbzg','vizxiucht4kt1crngeamjy8x','r2wjix91yhunijd26fhbykm8']
dyn=[k for k,v in items.items() if v[1]=='Click to edit']
falt=[ (k,v) for k,v in items.items() if k not in allids and k not in menu and k not in dyn]
assert not falt, falt
def sel(ids,pre=''):
    w=max(len(f'{pre}[data-itemid="{i}"]') for i in ids)
    lines=[]
    for n,i in enumerate(ids):
        s=f'{pre}[data-itemid="{i}"]'+(',' if n<len(ids)-1 else '')
        g,c=items[i]; lines.append(f'{s.ljust(w+2)}/* {g} · {c[:42]} */')
    return '\n'.join(lines)
VAR={'orange':'var(--px-orange)','red':'var(--px-red)','yellow':'var(--px-yellow)','blue':'var(--px-blue)','green':'var(--px-green)','violet':'var(--px-violet)','neutral':'#cfd6df'}
TIT={'orange':'Deuda, facturas y pagos','red':'Reclamos y soporte técnico','yellow':'Energía y suministros','blue':'Agua, información y reintentos',
     'green':'Internet y confirmaciones','violet':'Trámites, tarifas y alta','neutral':'Opciones secundarias'}
out=['','/* =====================================================================',
'   Botones de los submenús (generado desde el export, 03-11-2026)',
'   Mismo criterio que el menú principal: la marca izquierda indica el',
'   área. En Reclamos, cada servicio usa su color: energía amarillo,',
'   agua azul, internet verde. Si se recrea un botón, cambia su ID.',
'   ===================================================================== */','',
'/* Color por defecto para botones sin categoría (p. ej. listas dinámicas',
'   de domicilios y de reclamos, cuyos IDs los genera Typebot) */',
':where(.typebot-buttons-input .typebot-button) { --accent: var(--cuecca-navy-2); }','']
for k,ids in C.items():
    out+= [f'/* {TIT[k]} */', sel(ids), f'  {{ --accent: {VAR[k]}; }}','']
out+=['/* Navegación (Volver / Salir): pie discreto, como "Cerrar sesión" */',
 sel(NAV,'.typebot-buttons-input ')+' {','  margin-top: 4px;','  color: var(--cuecca-muted);','  font-weight: 400;','  font-size: 0.88rem;','}',
 sel(NAV,'.typebot-buttons-input ').replace(',\n',':: ,\n').replace(':: ,','::before,')+'::before { content: none; }' ,'']
navb=',\n'.join(f'.typebot-buttons-input [data-itemid="{i}"]::before' for i in NAV)
out[-2]=navb+' {\n  content: none;\n}'
out+=['/* Volver/Salir ya traen su emoji: sin flecha extra */',
 ',\n'.join(f'.typebot-buttons-input [data-itemid="{i}"]::after' for i in NAV)+' {\n  content: none;\n}','']
css=t['theme']['customCss']
marker='/* ---------- Valoración: estrellas en naranja del logo ---------- */'
assert marker in css
ini=css.find('/* =====================================================================\n   Botones de los submenús')
if ini!=-1:
    css=css[:ini]+css[css.find(marker):]   # regenerar: quita la sección anterior
# El color por defecto usa :where() (especificidad 0) para no pisar los [data-itemid]
new='\n'.join(out)
t['theme']['customCss']=css.replace(marker,new+'\n'+marker)
json.dump(t,open(sys.argv[2],'w'),ensure_ascii=False,indent=2)
open(sys.argv[3],'w').write(t['theme']['customCss'])
print(len(allids),'botones', 'dyn',len(dyn))

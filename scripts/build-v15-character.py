import numpy as np, trimesh, math
from pathlib import Path
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals
OUT=Path('assets');OUT.mkdir(exist_ok=True)
sc=trimesh.Scene()
cols={'skin':'#EAB391','skin_shade':'#D99B7C','blush':'#DB908E','hair':'#3A3039','hair_high':'#57444C','iris':'#756053','pupil':'#282E36','eye':'#FEF9EE','eyeline':'#473B43','jacket':'#638582','jacket_light':'#81A19A','jacket_dark':'#436B68','shirt':'#F6E8D5','pants':'#434D60','shoes':'#DFD4C7','sole':'#AEB4B3','gold':'#D7AD73','pink':'#B87377'}
mats={}
for k,c in cols.items():
 h=c.lstrip('#');mats[k]=PBRMaterial(name=k,baseColorFactor=tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,),metallicFactor=0,roughnessFactor=.88)
def T(x=0,y=0,z=0):
 m=np.eye(4);m[:3,3]=(x,y,z);return m
sc.graph.update(frame_to='CharacterRoot',frame_from=sc.graph.base_frame,matrix=T())
pivots={'Body':('CharacterRoot',(0,0,0)),'HeadPivot':('Body',(0,2.84,0)),'LeftArm':('Body',(-.40,2.5,0)),'RightArm':('Body',(.4,2.5,0)),'LeftLeg':('CharacterRoot',(-.17,1.51,0)),'RightLeg':('CharacterRoot',(.17,1.51,0))}
for n,(p,v) in pivots.items():sc.graph.update(frame_to=n,frame_from=p,matrix=T(*v))
i=0
def add(mesh,color,name,parent='Body'):
 global i
 i+=1;mesh.visual=TextureVisuals(material=mats[color]);sc.add_geometry(mesh,node_name=f'{name}_{i}',geom_name=f'{name}_{i}',parent_node_name=parent)
def ell(x,y,z,rx,ry,rz,c,name,p='Body'):
 mesh=trimesh.creation.icosphere(subdivisions=2);mesh.apply_scale([rx,ry,rz]);mesh.apply_translation([x,y,z]);add(mesh,c,name,p)
def loft(rings,color,name,p='Body',N=28):
 v=[];f=[]
 for y,x,z,rx,rz in rings:
  for k in range(N):
   a=2*math.pi*k/N;v.append((x+math.cos(a)*rx,y,z+math.sin(a)*rz))
 for j in range(len(rings)-1):
  for k in range(N):
   a=j*N+k;b=j*N+(k+1)%N;c=(j+1)*N+k;d=(j+1)*N+(k+1)%N
   f.extend([(a,b,c),(b,d,c)])
 v.extend([(rings[0][1],rings[0][0],rings[0][2]),(rings[-1][1],rings[-1][0],rings[-1][2])])
 lo,hi=len(v)-2,len(v)-1
 for k in range(N):
  f.append((lo,k,(k+1)%N));a=(len(rings)-1)*N+k;b=(len(rings)-1)*N+(k+1)%N;f.append((hi,b,a))
 mesh=trimesh.Trimesh(vertices=v,faces=f,process=False);mesh.fix_normals();add(mesh,color,name,p)
def tube(points,radius,c,name,p='Body',N=8):
 v=[];f=[];pts=np.array(points,float)
 for j,pos in enumerate(pts):
  vec=pts[min(len(pts)-1,j+1)]-pts[max(0,j-1)];vec/=np.linalg.norm(vec)+1e-9
  normal=np.cross(vec,[0,1,0])
  if np.linalg.norm(normal)<.0001:normal=np.cross(vec,[0,0,1])
  normal/=np.linalg.norm(normal);bn=np.cross(vec,normal)
  for k in range(N):
   a=math.tau*k/N;v.append(pos+radius*(math.cos(a)*normal+math.sin(a)*bn))
 for j in range(len(pts)-1):
  for k in range(N):
   a=j*N+k;b=j*N+(k+1)%N;c0=(j+1)*N+k;d=(j+1)*N+(k+1)%N;f.extend([(a,b,c0),(b,d,c0)])
 mesh=trimesh.Trimesh(vertices=v,faces=f,process=False);mesh.fix_normals();add(mesh,c,name,p)
def ribbon(pts,widths,c,name):
 v=[];f=[];pts=np.array(pts,float);N=9
 for j,pos in enumerate(pts):
  d=pts[min(len(pts)-1,j+1)]-pts[max(0,j-1)];n=np.cross(d,[0,0,1])
  if np.linalg.norm(n)<.001:n=np.array([1.,0,0])
  n/=np.linalg.norm(n)
  for k in range(N):
   q=k/(N-1)*2-1;v.append(pos+n*q*widths[j]+[0,0,.025*(1-q*q)])
 for j in range(len(pts)-1):
  for k in range(N-1):
   a=j*N+k;b=a+1;c0=(j+1)*N+k;d=c0+1;f.extend([(a,c0,b),(b,c0,d)])
 m=trimesh.Trimesh(vertices=v,faces=f,process=False);m.fix_normals();add(m,c,name,'HeadPivot')
loft([(1.48,0,0,.265,.169),(1.60,0,0,.276,.182),(1.96,0,0,.288,.175),(2.36,0,0,.357,.205),(2.52,0,-.008,.295,.16)],'shirt','Torso')
loft([(1.46,0,-.035,.280,.194),(1.57,0,-.04,.301,.204),(1.96,0,-.038,.308,.205),(2.39,0,-.03,.382,.225),(2.56,0,-.032,.273,.17)],'jacket','Jacket_Silhouette')
loft([(1.60,0,.176,.105,.032),(1.87,0,.205,.11,.032),(2.3,0,.215,.14,.035),(2.5,0,.156,.08,.024)],'shirt','Shirt_Front')
for side in [-1,1]:
 tube([[side*.12,2.46,.20],[side*.22,2.28,.246],[side*.118,2.045,.240]],.044,'jacket_light','Lapel')
for y in [1.81,1.99,2.17]:ell(.135,y,.228,.013,.015,.01,'gold','Button')
tube([[-.34,1.83,.155],[-.22,1.82,.231]],.008,'jacket_dark','Pocket')
ell(-.28,2.27,.192,.024,.028,.012,'gold','EmployeeBadge')
loft([(2.50,0,0,.108,.095),(2.80,0,0,.112,.100),(2.85,0,0,.126,.107)],'skin','Neck')
for side,parent in [(-1,'LeftArm'),(1,'RightArm')]:
 loft([(-.77,side*.07,.04,.09,.107),(-.62,side*.09,.042,.095,.107),(-.35,side*.075,0,.105,.115),(-.09,side*.025,0,.137,.139),(.04,0,0,.145,.146)],'jacket','Sleeve',parent,24)
 loft([(-.81,side*.08,.045,.096,.110),(-.75,side*.07,.045,.097,.110)],'shirt','Cuff',parent,20)
 ell(side*.082,-.902,.055,.084,.14,.077,'skin','Hand',parent)
for side,parent in [(-1,'LeftLeg'),(1,'RightLeg')]:
 loft([(-1.23,side*.026,.004,.125,.132),(-.95,side*.028,0,.13,.13),(-.60,side*.026,-.014,.148,.147),(-.27,side*.013,-.012,.175,.160),(.06,0,-.01,.170,.156)],'pants','Trouser',parent)
 ell(side*.023,-1.326,.134,.15,.115,.25,'shoes','Loafer',parent)
 ell(side*.023,-1.397,.143,.157,.037,.256,'sole','Sole',parent)
 tube([[side*.023-.08,-1.265,.329],[side*.023,-1.26,.361],[side*.023+.08,-1.265,.329]],.013,'jacket_dark','ShoeEdge',parent)
loft([(-.34,0,.03,.19,.13),(-.23,0,.02,.264,.205),(-.08,0,-.01,.332,.254),(.12,0,-.018,.356,.283),(.32,0,-.023,.331,.270),(.42,0,-.05,.253,.210)],'skin','Face','HeadPivot',40)
ell(0,-.23,.205,.20,.079,.067,'skin','Chin','HeadPivot')
for side in [-1,1]:
 ell(side*.335,-.038,-.038,.067,.104,.064,'skin','Ear','HeadPivot')
 ell(side*.145,.075,.259,.097,.065,.045,'eye','EyeWhite','HeadPivot')
 ell(side*.153,.073,.294,.05,.054,.023,'iris','Iris','HeadPivot')
 ell(side*.154,.071,.309,.032,.042,.013,'pupil','Pupil','HeadPivot')
 ell(side*.170,.092,.32,.014,.017,.006,'eye','EyeLight','HeadPivot')
 tube([[side*.07,.132,.279],[side*.153,.157,.286],[side*.234,.130,.257]],.012,'eyeline','EyeLid','HeadPivot')
 tube([[side*.069,.247,.244],[side*.14,.263,.268],[side*.235,.234,.227]],.013,'hair','Brow','HeadPivot')
 ell(side*.255,-.11,.222,.063,.035,.015,'blush','Blush','HeadPivot')
ell(0,-.06,.272,.026,.042,.041,'skin_shade','Nose','HeadPivot')
tube([[-.083,-.188,.256],[-.045,-.211,.277],[0,-.218,.282],[.045,-.211,.277],[.083,-.188,.256]],.011,'pink','Smile','HeadPivot')
loft([(.18,0,-.08,.345,.27),(.31,0,-.065,.345,.268),(.44,0,-.065,.315,.245),(.51,0,-.062,.17,.12)],'hair','HairCrown','HeadPivot',44)
loft([(-.43,0,-.16,.24,.17),(-.25,0,-.15,.29,.18),(.08,0,-.12,.36,.215),(.38,0,-.09,.345,.22)],'hair','BackHair','HeadPivot')
for side in [-1,1]:
 loft([(-.34,side*.32,-.11,.084,.125),(-.10,side*.343,-.095,.10,.13),(.12,side*.345,-.07,.103,.13),(.38,side*.29,-.055,.092,.11)],'hair','SideHair','HeadPivot',20)
ribbon([[-.31,.30,.164],[-.245,.21,.252],[-.115,.16,.277],[-.025,.205,.264]],[.085,.11,.09,.018],'hair','FringeLeft')
ribbon([[.30,.29,.158],[.26,.22,.230],[.22,.11,.262],[.30,.015,.209]],[.08,.10,.09,.035],'hair','FringeRight')
ribbon([[-.26,.41,.07],[-.09,.48,.17],[.08,.46,.188],[.21,.34,.15]],[.05,.095,.10,.025],'hair_high','HairHighlight')
ell(.306,.259,.17,.065,.016,.013,'gold','HairPin','HeadPivot')
blob=sc.export(file_type='glb')
(OUT/'yu-v15.glb').write_bytes(blob)
print('V15 GLB exported',len(blob),'bytes /',len(sc.geometry),'meshes')

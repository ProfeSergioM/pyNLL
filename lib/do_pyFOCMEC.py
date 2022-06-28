def do_pyFOCMEC(year,idev,nerrores,angle,evsel):
    focmecinput='FOCMEC.inp'
    focmecoutput='saved_locs/'+str(idev)+'_result'
    import subprocess
    from pyrocko.plot import beachball
    from lib import obtener_evento
    import os,stat
    try:
        os.remove('./focmec_run.sh')
    except:
        ()
        
    file=str(idev)+'.hyp'
    lines=[]
    with open("./loc/"+file) as file_in: 
        for line in file_in:
            lines.append(line)    
    i=0
    for line in lines:
        if line[0:5]=='PHASE':
            first_phase=i+1
        if line[0:9]=='END_PHASE':
            last_phase=i
        i+=1
            
    fases_lines = lines[first_phase:last_phase]
    head = lines[2]
    
    fases=[]
    for fase in fases_lines:
        splitted=fase.split()
        if splitted[5]!='?':
            fases.append(splitted[0]+splitted[23].rjust(8)+splitted[25].rjust(8)+splitted[5])
            
            
    
    file = open(focmecinput, "w") 
    with open('./FOCMEC.inp', 'a') as the_file:
        the_file.write(head)
        for fase in fases:
            the_file.write(fase+'\n')
            
    import subprocess
    
    
    p=subprocess.Popen(['/opt/focmec/bin/focmec'],
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE)

    
    p.stdin.write(b'focmec.lst\n')
    p.stdin.write(b'algo\n')
    p.stdin.write(b'FOCMEC.inp\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    p.stdin.write(b'\n')
    outputlog,errorlog = p.communicate()
    p.stdin.close()
    

    
    import sys
    evento = obtener_evento.obtener_evento(year,idev)[0]
    sys.path.append('/mnt/puntodiez/pyOvdas_lib')
    import ovdas_getfromdb_lib as gdb        
    volcanes =gdb.get_metadata_volcan(evento.idvolc.iloc[0],rep='y')
    voldf = volcanes.drop_duplicates(subset='nombre', keep="first")    
    import shutil
    filename=voldf.nombre_db.iloc[0]+'_'+str(evsel.fecha.iloc[0])[0:19].replace(' ','T').replace(':','-')+'_'+evsel.tipoevento.iloc[0]
    shutil.copy('focmec.lst','saved_locs/'+filename+'_result.lst')
    shutil.copy('focmec.lst','/mnt/puntocientodos/tmp/pyNLL/'+filename+'_result_FOCMEC.lst')
    
    
    #%%
    sta = open('FOCMEC.inp').read().splitlines()
    sta = sta[1:]
    stas = []
    for line in sta:
        stas.append([float(line.split()[1]),float(line.split()[2][:-1]),(line.split()[2][-1]),line.split()[0]])
    #%%
    
    mf =  open('saved_locs/'+filename+'_result.lst').read().splitlines()
    mp=[]
    ap=[]
    for i in range(0,len(mf)):
        if (mf[i][51:66]) == 'Auxiliary Plane':
            main = (mf[i-1].split())
            aux = (mf[i].split())
            mainp = [float(main[2]),float(main[1]),float(main[3])]
            auxp  = [float(aux[2]),float(aux[1]),float(aux[3])]
            mp.append(mainp)
            ap.append(auxp)
    
    
    import numpy as np
    desv_strike= np.std([x[0] for x in ap])
    desv_dip= np.std([x[1] for x in ap])
    desv_rake= np.std([x[2] for x in ap])
    
    
    
    
    #%%

    
    
    import numpy as np
    import mplstereonet
    import matplotlib.pyplot as plt
    
    fig = plt.figure(figsize=(6,4))
    
    ax = fig.add_subplot(111, projection='stereonet')
    
    
    from pyrocko import moment_tensor as pmt
    
    j=0
    for mecs in mp:
        lw=1
        al=0.2
    
        mt = pmt.MomentTensor(strike=mecs[0],dip=mecs[1],rake=mecs[2])
        beachball.plot_beachball_mpl(
            mt,ax,
            # type of beachball: deviatoric, full or double couple (dc)
            beachball_type='full',
            size=220,
            position=(0,0),
            alpha=al,
            linewidth=lw)
        j=j+1
        
        
        
        
    k=1
    for sta in stas:
        if sta[2]=='C':
            marker='$'+str(k)+'c$'
        elif sta[2]=='D':
            marker='$'+str(k)+'d$'
        else:
            marker='o'
        ax.pole(sta[0]+90,sta[1],marker=marker,markersize=15,color='k', clip_on=False,label=sta[3])
        k=k+1
        
        
    ax.set_azimuth_ticks([])
    ax.legend(loc=(1,0.25))
    ax.text(0.05,0.05,'Strike:'+str(int(mecs[0]))+'°, Dip:'+str(int(mecs[1]))+
            '°, Rake:'+str(int(mecs[2]))+'°',ha='left',
            transform=fig.transFigure,
            bbox=dict(boxstyle="round",
                       ec=(1., 0.5, 0.5),
                       fc=(1., 0.8, 0.8),
                       ))

    ax.text(0.95,0.05,'δ Strike:'+str(np.round(desv_strike,1))+'°, δ Dip:'+str(np.round(desv_dip,1))+
            '°, δ Rake:'+str(int(np.round(desv_rake,1)))+'°',
            transform=fig.transFigure,ha='right',
            bbox=dict(boxstyle="round",
                       ec=(1., 0.5, 0.5),
                       fc=(1., 0.8, 0.8),
                       ))
    mt = pmt.MomentTensor(strike=mecs[0],dip=mecs[1],rake=mecs[2])
    beachball.plot_beachball_mpl(
        mt,ax,
        # type of beachball: deviatoric, full or double couple (dc)
        beachball_type='full',
        size=220,
        position=(0,0),
        alpha=al,
        linewidth=10)

    
    evento = obtener_evento.obtener_evento(year,idev)[0]
    
    fecha = str(evento.fecha.iloc[0])[:-7]
    
    ax.text(0.1,0.95,'Fecha: '+fecha,transform=fig.transFigure,ha='left')
    ax.text(0.95,0.95,'Id Evento: '+str(idev),transform=fig.transFigure,ha='right')
    ax.text(0.1,0.9,'Volcán :'+str(voldf.nombre_db.iloc[0]),transform=fig.transFigure,ha='left')



    plt.savefig('saved_locs/'+filename+'_pyFOCMEC.png',dpi=200)
    plt.close('all')
    import shutil

    shutil.copyfile('saved_locs/'+filename+'_pyFOCMEC.png', '/mnt/puntocientodos/tmp/pyNLL/'+filename+'_pyFOCMEC.png')
    plt.close('all')
    import shutil,os
    try:
        shutil.move(str(idev)+'_result.lst','saved_locs/'+str(idev)+'_result.lst')
        shutil.move(str(idev)+'_result.out','saved_locs/'+str(idev)+'_result.out')
        os.remove('a.junk')
        os.remove('focmec_run.sh')
    except:
        ()

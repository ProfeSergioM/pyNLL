#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:36:29 2021

@author: sergio.morales
"""

def plot_loc_syn(randomint,evloc,df_sta,nref,zmax):
    
    import numpy as np
    filename='loc/'+str(randomint)+'.hyp'
    
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        
    scatter=[]
    go=False
    for line in lines:
        if line[0:7]=='SCATTER':
            go=True
        if go==True:
            scatter.append(line)
    scatter2=scatter[1:-3]
    
    PDF=[]
    
    for line in scatter2:
        PDF.append(float(line.split()[3]))
    
    PDF = np.array(PDF)   
    

    from obspy import read_events
    import pandas as pd
    cat = read_events("loc/last.hyp") 
    import ovdas_getfromdb_lib as gdb
    volnet = gdb.get_metadata_wws(volcan='*')
    volnet = volnet[volnet.tipo=='SISMOLOGICA']
    estas,fases =[],[]
    for i in range(0,len(cat[0].picks)):
        esta = cat[0].picks[i].waveform_id.station_code
        fase = cat[0].picks[i].phase_hint
        estas.append(esta[:-1])
        fases.append(fase)
    #estadf = pd.DataFrame([estas,fases]).T
    import numpy as np
    import matplotlib
    import sys
    sys.path.append('//172.16.40.10/sismologia/pyovdas_lib/')
    import ovdas_getfromdb_lib as gdb
    from obspy import read_events
    cat = read_events("loc/last.hyp")
    lonN=cat[0].origins[0].longitude
    latN=cat[0].origins[0].latitude
    profN=cat[0].origins[0].depth/1000
    erlonN =cat[0].origins[0].longitude_errors.uncertainty
    erlatN =cat[0].origins[0].latitude_errors.uncertainty
    erproN = cat[0].origins[0].depth_errors.uncertainty/1000
    def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
        new_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
            cmap(np.linspace(minval, maxval, n)))
        return new_cmap
    from math import cos, radians
    PDF_lonlatXY= pd.read_csv('loc/'+str(randomint)+'.scat.lonlat.XY',header=None,sep=' ')
    PDF_lonlatXY = PDF_lonlatXY.rename(columns={0:'lon',1:'lat'})
    PDF_lonlatXZ= pd.read_csv('loc/'+str(randomint)+'.scat.lonlat.XZ',compression=None,header=None,sep=' ')
    PDF_lonlatXZ = PDF_lonlatXZ.rename(columns={0:'lon',1:'prof'})
    df_PDF = pd.DataFrame([PDF_lonlatXZ['lon'],PDF_lonlatXY['lat'],PDF_lonlatXZ['prof']]).T
    
    df_PDF['PDF']=(PDF-min(PDF))/(max(PDF)-min(PDF))
    
    
    
    dlon = df_PDF.lon.max()-df_PDF.lon.min()
    dlat = df_PDF.lat.max()-df_PDF.lat.min()
    #londelta = max(dlon,dlat)*2
    londelta=latdelta=np.round(max(dlon,dlat)*2/110,3)
    loncenter=evloc[1]
    latcenter=evloc[0]
    #aspect_ratio = 1/cos(radians(latcenter))
    #latdelta = londelta/aspect_ratio
    
  
    
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(10,10))
    gs = gridspec.GridSpec(2, 2,width_ratios=[5,9],height_ratios=[9,5])
    gs.update(left=0.1, right=0.9,top=0.95,bottom=0.09, wspace=0.03, hspace=0.03)
    londelta=latdelta=max(abs(evloc[0]-df_sta.stalat).max(),abs(evloc[1]-df_sta.stalon).max())*1.1
    mapa1 = fig.add_subplot(gs[1],projection=ccrs.PlateCarree())
    mapa1.set_extent([evloc[1]-londelta,evloc[1]+londelta,
                     evloc[0]-latdelta,evloc[0]+latdelta],
                    crs=ccrs.PlateCarree())
    
    ###mapa de fondo
    import cartopy.crs as ccrs
    import cartopy.io.img_tiles as cimgt
    #stamen_terrain = cimgt.Stamen('terrain')
    #mapa1.add_image(stamen_terrain, 10)
    
    
    mapa1.set_adjustable('datalim')
    plt.draw()
    x0,x1,y0,y1 = mapa1.get_extent(ccrs.PlateCarree())
    
    mapa1_proflat = fig.add_subplot(gs[0])
    
    mapa1_proflat.set_ylim(y0,y1)
    mapa1_proflat.grid(True,linestyle='--',alpha=0.5,linewidth=0.5,color='black')
    
    mapa1_proflon = fig.add_subplot(gs[3])
    
    mapa1_proflon.set_xlim(x0,x1)
    
    
    mapa1_proflon.grid(True,linestyle='--',alpha=0.5,linewidth=0.5,color='black')
    
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    
    
    if zmax=='-':
        zlim = max((cat[0].origins[0].depth/1000),df_PDF.prof.max())
    else:
        zlim = int(zmax)/2
    if zlim<0:zlim=0
    elif zlim<1:zlim=3
    else:zlim=zlim*2
    import matplotlib.ticker as ticker
    mapa1.set_aspect('auto')
    gl = mapa1.gridlines(crs=ccrs.PlateCarree(), linewidth=0.5, color='black', alpha=0.5, linestyle='--', draw_labels=False)
    gl.xlocator = ticker.MultipleLocator(0.1)
    gl.ylocator = ticker.MultipleLocator(0.1)
    
    mapa1_proflon.set_ylim(zlim,-nref/1000)
    mapa1_proflat.set_xlim(zlim,-nref/1000)
    mapa1_proflat.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    mapa1_proflon.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
    
    
    
    #mapa1.plot(df_PDF['lon'],df_PDF['lat'],'.',ms=1,lw=0,alpha=0.2,label='PDF')
    scat = mapa1.scatter(df_PDF['lon'],df_PDF['lat'],s=1,c=df_PDF['PDF'])
    
    
    
    #mapa1_proflat.plot(df_PDF['prof'],df_PDF['lat'],'.',ms=1,lw=0,alpha=0.2,label='PDF')
    #mapa1_proflon.plot(df_PDF['lon'],df_PDF['prof'],'.',ms=1,lw=0,alpha=0.2,label='PDF')
    mapa1_proflat.scatter(df_PDF['prof'],df_PDF['lat'],s=1,c=df_PDF['PDF'])
    mapa1_proflon.scatter(df_PDF['lon'],df_PDF['prof'],s=1,c=df_PDF['PDF'])
    
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes


    
    axins = inset_axes(mapa1,                  width="5%",  # width = 5% of parent_bbox width
                   height="50%",  # height : 50%
                   loc='lower left',
                   bbox_to_anchor=(1.03, 0., 1, 1),
                   bbox_transform=mapa1.transAxes,
                   borderpad=0,
                   )
    cbar = fig.colorbar(scat, cax=axins, orientation="vertical")    
    cbar.set_label('Calidad de localización normalizada')
    
    
    mapa1.plot(evloc[1],evloc[0],'*',mfc='C3',markersize=10,mec='k',label='Sintético')
    mapa1.plot(lonN,latN,marker='*',mfc='C2',markersize=10,lw=0,mec='k',label='Loc NLL')
    
    mapa1_proflat.plot(evloc[2],evloc[0],'*',mfc='C3',markersize=10,mec='k',label='Sintetico')
    mapa1_proflat.plot(profN,latN,marker='*',mfc='C2',markersize=10,mec='k',label='Loc NLL Syn')
    mapa1_proflon.plot(evloc[1],evloc[2],'*',mfc='C3',markersize=10,mec='k',label='Sintetico')
    mapa1_proflon.plot(lonN,profN,marker='*',mfc='C2',markersize=10,mec='k',label='Loc NLL Syn')
    
    for index,row in df_sta.iterrows():
        if row.tipoest=='ovd':
            colors='C3'
        elif row.tipoest=='syn':
            colors='C4'
        if row.faseP==True:
            mapa1.plot(row.stalon,row.stalat,'o',ms=6,color=colors,fillstyle='top',label='Fase P')
            mapa1_proflat.plot(-row.staele/1000,row.stalat,'o',ms=6,color=colors,fillstyle='top',label='Fase P')
            mapa1_proflon.plot(row.stalon,-row.staele/1000,'o',ms=6,color=colors,fillstyle='top',label='Fase P')
        if row.faseS==True:
            mapa1.plot(row.stalon,row.stalat,'o',ms=6,color=colors,fillstyle='full',label='Fase S')
            mapa1_proflon.plot(row.stalon,-row.staele/1000,'o',ms=6,color=colors,fillstyle='full',label='Fase S')
            mapa1_proflat.plot(-row.staele/1000,row.stalat,'o',ms=6,color=colors,fillstyle='full',label='Fase S')
    
    handles, labels = mapa1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    leg = mapa1.legend(by_label.values(), by_label.keys(),frameon=True)
    i=0
    #for lh in leg.legendHandles: 
    #    if i==0:
    #        lh._legmarker.set_markersize(10)
    #    lh._legmarker.set_alpha(1)
    #    i+=1
        
    mapa1_proflat.set_ylabel('Latitud (°)')
    mapa1_proflat.set_xlabel('Profundidad (km)')
    mapa1_proflon.set_ylabel('Profundidad (km)')
    mapa1_proflon.set_xlabel('Longitud (°)')
    mapa1_proflon.yaxis.set_label_position("right")
    mapa1_proflon.yaxis.tick_right()
    
    mapa1_proflat.xaxis.set_label_position("top")
    mapa1_proflat.xaxis.tick_top()
    
    mapa1_texto = fig.add_subplot(gs[2])
    mapa1_texto.axis('off')
    mapa1_texto.table(cellText=[
                                ['','Latitud','Longitud','Prof.\n(km)'],
                                ['Sint.',str(evloc[0])+'°',str(evloc[1])+'°',str(evloc[2])],
                                ['Loc NLL',str(np.round(latN,4)),str(np.round(lonN,4)),str(np.round(profN,4))],
                                ['Error\n+/-',str(np.round(erlatN,4))+'°',str(np.round(erlonN,4))+'°',
                                 str(np.round(erproN,4))],
                                
                                ['Difer.',str(np.round(abs(evloc[0]-latN),4)),str(np.round(abs(evloc[1]-lonN),4)),
                                 str(np.round(abs(evloc[2]-profN),4))]
    
     
                                        
                            
                                ],
                      colWidths=[0.25,0.3,0.3,0.3],
                              bbox = [0,0,1,1],zorder=1, rasterized=True) 
    
    mapa1.set_title('Resultado de localización de evento sintético',fontsize=12)
    plt.savefig('syn_loc_'+str(randomint)+'.png',dpi=200)
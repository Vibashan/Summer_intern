import math

(xp,yp) = (400,100)
(xe,ye) = (300,600)
(xt,yt) = (50,60) 


def pur_eva(xp,yp,xe,ye,xt,yt):
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2

    xi = (s*(ym-yt)-(s*s)*xt+xm)/((s*s)+1)
    yi = yt+s*xt+xi

    wp = math.atam2((yi-yp),(xi-xp))
    we = math.atan2((yi-ye),(xi-xe))
    vx_p = 1*math.cos(wp)
    vy_p = 1*math.sin(wp)
    vx_e = 1*math.cos(we)
    vy_e = 1*math.cos(we)
    return vx_p,vy_p,vx_e,vy_e

vx_p,vy_p,vx_e,vy_e = pur_eva(xp,yp,xe,ye,xt,yt)
print(vx_p,vy_p,vx_e,vy_e)
import math

(xp,yp) = (100,200)
(xe,ye) = (500,400)
(xt,yt) = (50,100)


def pur_eva(xp,yp,xe,ye,xt,yt):
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2

    xi = (s*(ym-yt)+(s*s)*xt+xm)/((s*s)+1)
    yi = yt-s*xt+s*xi
    print(xi,yi)

    wp = math.atan2((yi-yp),(xi-xp))
    we = math.atan2((yi-ye),(xi-xe))
    vx_p = 1*math.cos(wp)
    vy_p = 1*math.sin(wp)
    vx_e = 1*math.cos(we)
    vy_e = 1*math.sin(we)
    return vx_p,vy_p,vx_e,vy_e

vx_p,vy_p,vx_e,vy_e = pur_eva(xp,yp,xe,ye,xt,yt)
print(vx_p,vy_p,vx_e,vy_e)
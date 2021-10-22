import numpy as np

class Aerodynamics:
    def __init__(self):
        self.density = 1.2148
        self.velocity = 22
        self.viscous = 1.78621e-5
        self.mach = 0.0588

    def lift_coef(self, MTOW, S):
        return (2*MTOW*9.81)/(self.density*self.velocity**2*S)

    def induced_drag_coef(self, Cl, e, AR):
        return (Cl**2)/(np.pi*e*AR)
    
    def reynold_number(self, L):
        return (self.density*self.velocity*L)/self.viscous

    def skin_friction_coef(self, Re):
        if(Re > 5e5):
            return (0.455/((np.log10(Re))**2.58)) - (1700/Re)
            # return (0.455/(((np.log10(Re))**2.58)*(1+(0.144*self.mach**2))**0.58))
        else:
            return 1.328/np.sqrt(Re)

    def oswald_efficiency_factor(self, AR):
        return (1.78*(1-0.045*AR**0.68))-0.64

    def aspect_ratio(self, b, S):
        return b**2/S
    
    def mean_aerodynamics_chord(self, cr, ct):
        return (2/3)*(cr+ct-((cr*ct)/(cr+ct)))

    def wing_area(self, b, mac):
        return b*mac
    
    def wing_form_factor(self, t_c, swept):
        swept = np.deg2rad(swept)
        a = (2*2.3*(t_c*np.cos(swept)**2))/np.sqrt(1-(self.mach**2*np.cos(swept)**2))
        b = (2.3**2*np.cos(swept)**2*t_c**2*(1+(5*np.cos(swept)**2)))/(2*(1-(self.mach*np.cos(swept))**2))
        return 1 + a + b

    def wing_weight(self, MTOW, S, b, t_c):
        A = 45.42*S
        B = 8.71e-5*((2.5*(b**3)*np.sqrt(25*MTOW*9.81**2))/(S*t_c))
        return (A + B)/9.81
    
    # def h_tail_weight(self, MTOW, S_h, b_h, mac, lv):
    #     A = 5.25*S_h
    #     B = 0.8e-6*((2.5*b_h**3*(MTOW)*mac*np.sqrt(S_h))/(0.09*lv*S_h**1.5))
    #     return (A + B)

    # def v_tail_weight(self, MTOW, S_v, S, b_v, swept_v):
    #     swept_v = np.deg2rad(swept_v)
    #     A = 2.62*S_v
    #     B = 1.5e-5*((2.5*b_v**3*(8+(0.44*((MTOW)/S))))/(0.09*np.cos(swept_v)**2))
    #     return (A + B)

    def total_drag(self, Cd0, Cdi):
        return Cd0 + Cdi

    def function(self, x):
        # Wing

        # MTOW = x[0]
        # taper_ratio = x[1]
        # swept = x[2]
        # t_c = x[3]
        # b = x[4]

        cr = x[4]/6
        ct = cr*x[1]
        mac = self.mean_aerodynamics_chord(cr, ct)
        S = self.wing_area(x[4], mac)
        AR = self.aspect_ratio(x[4], S)
        e = self.oswald_efficiency_factor(AR)

        Cl = self.lift_coef(x[0], S)
        Re = self.reynold_number(mac)
        Cf = self.skin_friction_coef(Re)

        Cdi = self.induced_drag_coef(Cl, e, AR)
        Cd0 = self.wing_form_factor(x[3], x[2])*Cf*2

        total_drag_wing = self.total_drag(Cd0, Cdi)

        # H_tail

        # t_c_h = x[5]
        # swept_h = x[6]

        b_h = np.sqrt(((2/3)*AR)*0.18)
        c_h = b_h/2.5
        mac_h = c_h

        Re_h = self.reynold_number(mac_h)
        Cf_h = self.skin_friction_coef(Re_h)
        Cd0_h = self.wing_form_factor(x[5], x[6])*Cf_h*((mac_h*b_h)/S)

        # V_tail

        # AR_v = x[7]
        # taper_ratio_v = x[8]
        # t_c_v = x[9]
        # swept_v = x[10]

        b_v = np.sqrt(x[7]*0.15)
        cr_v = b_h/2.5
        ct_v = cr_v*x[8]
        mac_v = self.mean_aerodynamics_chord(cr_v, ct_v)

        Re_v = self.reynold_number(mac_v)
        Cf_v = self.skin_friction_coef(Re_v)
        Cd0_v = self.wing_form_factor(x[9], x[10])*Cf_v*((mac_v*b_v)/S)

        # total_drag_coef
        total_drag_coef = total_drag_wing + Cd0_h + Cd0_v

        return total_drag_coef

    def result(self, x):
        # Wing

        # MTOW = x[0]
        # taper_ratio = x[1]
        # swept = x[2]
        # t_c = x[3]
        # b = x[4]

        cr = x[4]/6
        ct = cr*x[1]
        mac = self.mean_aerodynamics_chord(cr, ct)
        S = self.wing_area(x[4], mac)
        AR = self.aspect_ratio(x[4], S)
        e = self.oswald_efficiency_factor(AR)

        Cl = self.lift_coef(x[0], S)
        Re = self.reynold_number(mac)
        Cf = self.skin_friction_coef(Re)

        Cdi = self.induced_drag_coef(Cl, e, AR)
        Cd0 = self.wing_form_factor(x[3], x[2])*Cf*2

        total_drag_wing = self.total_drag(Cd0, Cdi)

        # H_tail

        # t_c_h = x[5]
        # swept_h = x[6]

        b_h = np.sqrt(((2/3)*AR)*0.18)
        c_h = b_h/2.5
        S_h = b_h*c_h
        mac_h = c_h

        Re_h = self.reynold_number(mac_h)
        Cf_h = self.skin_friction_coef(Re_h)
        Cd0_h = self.wing_form_factor(x[5], x[6])*Cf_h*((mac_h*b_h)/S)

        # V_tail

        # AR_v = x[7]
        # taper_ratio_v = x[8]
        # t_c_v = x[9]
        # swept_v = x[10]

        b_v = np.sqrt(x[7]*0.15)
        cr_v = b_h/2.5
        ct_v = cr_v*x[8]
        mac_v = self.mean_aerodynamics_chord(cr_v, ct_v)
        S_v = b_v*mac_v

        Re_v = self.reynold_number(mac_v)
        Cf_v = self.skin_friction_coef(Re_v)
        Cd0_v = self.wing_form_factor(x[9], x[10])*Cf_v*((mac_v*b_v)/S)
        lv = 1.34-mac*0.25-mac_v*0.75

        w_wing = self.wing_weight(x[0], S, x[4], x[3])
        w_h_tail = self.wing_weight(x[0], S_h, b_h, x[5])
        w_v_tail = self.wing_weight(x[0], S_v, b_v, x[9])
        # w_h_tail = self.h_tail_weight(x[0], S_h, b_h, mac, lv)
        # w_v_tail = self.v_tail_weight(x[0], S_v, S, b_v, x[8])


        # total_drag_coef
        total_drag_coef = total_drag_wing + Cd0_h + Cd0_v

        return (
            x[0], #0
            cr, #1
            ct, #2
            x[1], #3
            x[2], #4
            x[4], #5
            mac, #6
            S, #7
            AR, #8
            e, #9
            Cl, #10
            Cdi, #11
            Cd0, #12
            x[5], #13
            x[6], #14
            b_h, #15
            c_h, #16
            Cd0_h, #17
            x[7], #18
            x[8], #19
            x[9], #20
            x[10], #21
            b_v, #22
            cr_v, #23
            ct_v, #24
            mac_v, #25
            Cd0_v, #26
            total_drag_coef, #27
            S_h, #28
            S_v, #29
            w_wing, #30
            w_h_tail, #31
            w_v_tail, #32
            lv #33
        )
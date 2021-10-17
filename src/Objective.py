import numpy as np

class Aerodynamics:
    def __init__(self):
        self.density = 1.2148
        self.velocity = 25
        self.viscous = 1.78621e-5
        self.mach = 0.0588

    def lift_coef(self, MTOW, S):
        return (2*MTOW*9.81)/(self.density*self.velocity**2*S)

    def induced_drag_coef(self, Cl, e, AR):
        return (Cl**2)/(np.pi*e*AR)
    
    def reynold_number(self, L):
        return (self.density*self.velocity*L)/self.viscous

    def skin_friction_coef(self, Re):
        return (0.455/(np.log10(Re))**2.58) - (1700/Re)

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
        Cd0 = self.wing_form_factor(x[3], x[2])*Cf*S

        total_drag_wing = self.total_drag(Cd0, Cdi)

        # H_tail

        # t_c_h = x[5]
        # swept_h = x[6]

        b_h = np.sqrt(((2/3)*AR)*0.22)
        c_h = b_h/3
        mac_h = c_h

        Re_h = self.reynold_number(mac_h)
        Cf_h = self.skin_friction_coef(Re_h)
        Cd0_h = self.wing_form_factor(x[5], x[6])*Cf_h*S

        # V_tail

        # AR_v = x[7]
        # taper_ratio_v = x[8]
        # t_c_v = x[9]
        # swept_v = x[10]

        b_v = np.sqrt(x[7]*0.15)
        cr_v = b_h/3
        ct_v = cr_v*x[8]
        mac_v = self.mean_aerodynamics_chord(cr_v, ct_v)

        Re_v = self.reynold_number(mac_v)
        Cf_v = self.skin_friction_coef(Re_v)
        Cd0_v = self.wing_form_factor(x[9], x[10])*Cf_v*S

        # total_drag_coef
        total_drag_coef = total_drag_wing + Cd0_h + Cd0_v*2

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
        Cd0 = self.wing_form_factor(x[3], x[2])*Cf*S

        total_drag_wing = self.total_drag(Cd0, Cdi)

        # H_tail

        # t_c_h = x[5]
        # swept_h = x[6]

        b_h = np.sqrt(((2/3)*AR)*0.22)
        c_h = b_h/2.5
        S_h = b_h*c_h
        mac_h = c_h

        Re_h = self.reynold_number(mac_h)
        Cf_h = self.skin_friction_coef(Re_h)
        Cd0_h = self.wing_form_factor(x[5], x[6])*Cf_h*S

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
        Cd0_v = self.wing_form_factor(x[9], x[10])*Cf_v*S

        # total_drag_coef
        total_drag_coef = total_drag_wing + Cd0_h + Cd0_v*2

        return (
            x[0], 
            cr, 
            ct, 
            x[1], 
            x[2], 
            x[4], 
            mac, 
            S, 
            AR, 
            e, 
            Cl, 
            Cdi, 
            Cd0, 
            x[5],
            x[6],
            b_h,
            c_h,
            Cd0_h,
            x[7],
            x[8],
            x[9],
            x[10],
            b_v,
            cr_v,
            ct_v,
            mac_v,
            Cd0_v,
            total_drag_coef,
            S_h,
            S_v
        )
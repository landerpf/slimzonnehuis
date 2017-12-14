class heating:
    def __init__(self,isolation_coef,wall_with,wall_surface,cop,air_mass,heating_capacity=710):
        self.__isolatian_coef=isolation_coef
        self.__wall_with=wall_with
        self.__wall_surface=wall_surface
        self.__cop=cop
        self.__air_mass=air_mass
        self.__capacity=heating_capacity
    def get_isolation_coef(self):
        return self.__isolatian_coef
    def get_wall_with(self):
        return self.__wall_with
    def get_wall_surface(self):
        return self.__wall_surface
    def get_cop(self):
        return self.__cop
    def get_air_mass(self):
        return self.__air_mass
    def get_capacity(self):
        return self.__capacity
    def apply_heating(self,remaining_energy,outside_temp_list,max_temp=19,min_temp=23,start_temp=21):
        u=self.get_isolation_coef()/self.get_wall_with()
        a=self.get_wall_surface()
        cop=self.get_cop()
        m=self.get_air_mass()
        c=self.get_capacity()
        time=1*15*60
        for t in range(0,len(remaining_energy)):

            outside_temp=outside_temp_list[t]
            inside_temp=start_temp
            delta_temp = outside_temp - inside_temp  # gaat vaak positief zijn
            if inside_temp<min_temp:
                t_op=max_temp-inside_temp
                qh=c*t_op*m/time+u*a*delta_temp
                w=qh/cop
                remaining_energy[t]-=w
                start_temp=max_temp
            elif inside_temp<max_temp:

                t_op = max_temp - inside_temp
                qh = c * t_op * m / time + u * a * delta_temp
                w = qh / cop
                if w<= remaining_energy[t]:
                    start_temp = max_temp
                    remaining_energy[t]-=w
                else:
                    w_real=remaining_energy[t]
                    t_op_real=time*w_real*cop*delta_temp/(c*m)
                    start_temp=max_temp-t_op_real
                    remaining_energy[t]-=w_real
            else:
                qv=u*a*delta_temp
                t_af=time*qv/(c*m)
                start_temp-=t_af

        return
def get_outside_temp():#nog nodig jens ging dit doen


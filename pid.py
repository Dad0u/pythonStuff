#coding: utf-8
import matplotlib.pyplot as plt


class PID(object):
    def __init__(self,P,I,D,**kwargs):
        self.global_limit = kwargs.get("global_limit",True)
        self.out_min = kwargs.get("min",-10)
        self.out_max = kwargs.get("max",10)
        #This will make sure the actual output
        #will always be between out_min and out_max
        # Because each influence (P,I and D) will be limited independantly
        if not self.global_limit:
            self.out_max /= 3
            self.out_min /= 3
        self.P = P
        self.I = I
        self.D = D
        self.out = 0
        self.nI = kwargs.get("ni",50) # Number of dots to compute intergal
        self.nD = kwargs.get("nd",6) # ...derivative
        self.hist = []

    def update(self,target,out_value):
        diff = target-out_value
        if len(self.hist) < max(self.nI,self.nD):
            self.hist.append(diff)
        else:
            self.hist = self.hist[1:]
            self.hist.append(diff)

        self.out = self.getP(target,out_value)\
                    +self.getI(target,out_value)\
                    +self.getD(target,out_value)

    def limit(self,val):
        return max(min(self.out_max,val),self.out_min)

    def getP(self,target,out_value):
        if self.global_limit:
            return self.P*(target-out_value)
        else:
            return self.limit(self.P*(target-out_value))

    def getI(self,target,out_value):
        val = self.I*sum(self.hist[-self.nI:])/len(self.hist[-self.nI:])
        if self.global_limit:
            return val
        else:
            return self.limit(val)

    def getD(self,target,out_value):
        assert self.nD%2 == 0,"nD must be even!"
        if len(self.hist) < self.nD:
            n = len(self.hist)//2
        else:
            n = self.nD//2
        val = self.D*(sum(self.hist[-n:])-
                       sum(self.hist[-2*n:-n]))/self.nD
        if self.global_limit:
            return val
        else:
            return self.limit(val)

    def get_cmd(self,target,out_value):
        self.update(target,out_value)
        if self.global_limit:
            return self.limit(self.out)
        else:
            return self.out


if __name__ == '__main__':
  """
  Testing with a fake motor
  """
  class FakeMotor(object):
      def __init__(self,**kwargs):
          self.inertia = kwargs.get("inertia",400)
          # A negative torque applied on the motor
          self.torque = kwargs.get("torque",0)
          self.kv = kwargs.get("kv",1000) # rpm/V
          self.rv = kwargs.get("rv",.4) # solid friction
          self.fv = kwargs.get("fv",2e-5) # fluid friction
          self.rpm = 0
          self.pos = 0
          self.u = 0 # V

      def update(self,t=1):
          """
          Will update the motor rpm after t ms
          Supposes u is constant for the interval t
          """
          F = self.u*self.kv-self.torque-self.rpm*(1+self.rv+self.rpm*self.fv)
          drpm = F/self.inertia*t
          self.pos += t*(self.rpm+drpm/2)
          self.rpm += drpm

      def set_u(self,u):
          self.u = u

  m = FakeMotor(torque=500)
  pid = PID(.1,.07,.283,min=-20,max=20,global_limit=True,ni=10)
  target = 10000
  t = []
  tar = []
  rpm = []
  cmd = []
  tp = []
  ti = []
  td = []
  pos = []

  for i in range(5000):

      if i <= 2000: # Ramp
          target = i
      if i == 2000: # Step
          target = 5000
      if i == 3000: # Torque step
          m.torque = 3500 # Change the counter torque on the motor
      if i == 4000: # Cut everything
          m.torque = 0
          pid = PID(0,0,0)

      curr_rpm = m.rpm
      curr_pos = m.pos
      curr_cmd = pid.get_cmd(target,curr_rpm)
      #curr_cmd = pid.get_cmd(target,curr_pos)

      m.set_u(curr_cmd)
      m.update()
      t.append(i)
      tar.append(target)
      rpm.append(curr_rpm)
      pos.append(curr_pos)
      cmd.append(200*curr_cmd)
      tp.append(pid.getP(target,curr_rpm))
      ti.append(pid.getI(target,curr_rpm))
      td.append(pid.getD(target,curr_rpm))

  #plt.plot(t,pos)
  plt.plot(t,rpm)
  plt.plot(t,cmd)
  plt.plot(t,tar)
  #plt.plot(t,t)
  plt.subplots()
  plt.plot(t,tp)
  plt.plot(t,ti)
  plt.plot(t,td)
  plt.show()

import numpy as np
from numpy.random import randn

class agent:
    def __init__(self,**kwargs):
        """Initialize agent class
        Keyword arguments:
        m_dims -- the indices of motor values
        s_dims -- the indices of sensory values
        ms_bounds -- the bounds of ms variable with shape (2, :) (2 for (min,max))
        sm_model -- the class of the sensorimotor model
        i_model -- the class of the interest model
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        for key, value in kwargs['space_args'].items():
            setattr(self, key, value)
        #self.m_dims=self.space_args['m_dims']
        #self.s_dims=self.space_args['s_dims']
        #self.ms_bounds=self.space_args['ms_bounds']
        self.ms_dims=self.m_dims + self.s_dims
        self.m_bounds=self.ms_bounds[:,self.m_dims]
        self.s_bounds=self.ms_bounds[:,self.s_dims]
        self.ms=np.zeros((len(self.ms_dims),1))
        self.sm_model=self.sm_model(**(self.sm_params))
        self.i_model=self.i_model(**self.i_params)
        m,s = self.env.execute(np.zeros((len(self.m_dims),1))) 
        self.sm_model.update(m, s)

    def explore(self, in_dims, out_dims):
        x = self.i_model.sample(in_dims)
        y = self.sm_model.infer(in_dims, out_dims, x)
        self.ms[in_dims]=x
        self.ms[out_dims]=y
        m=self.ms[self.m_dims].reshape(len(self.m_dims),1)
        m,s = self.env.execute(m) 
        s += self.noise*randn(len(self.s_dims),1)
        comp = self.competence(self.ms[self.s_dims], s)
        self.sm_model.update(m, s)
        self.i_model.update(x,comp)
        return x,y,m,s,comp
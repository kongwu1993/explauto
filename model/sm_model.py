import numpy as np
import imle as imle_

class SmModel(object):
    def __init__(self, m_dims, s_dims):
        self.m_dims=m_dims
        self.s_dims=s_dims

    def infer(self, in_dims, out_dims):
        raise NotImplementedError

    def update(self, m, s):
        raise NotImplementedError


class ImleModel(SmModel):
    def __init__(self, m_dims, s_dims, sigma0, psi0):
        SmModel.__init__(self, m_dims, s_dims)
        self.imle=imle_.Imle(in_ndims=len(m_dims), out_ndims=len(s_dims), 
                sigma0=sigma0, Psi0=psi0)

    def infer(self, in_dims, out_dims,x):
        if in_dims == self.s_dims and out_dims==self.m_dims:
            try:
                sols = self.imle.predict_inverse(x.flatten())
                return sols[np.random.randint(len(sols))].reshape(-1,1)
            except RuntimeError as e:
                print e
                return self.imle.to_gmm().inference(in_dims, out_dims, x).sample().T
        elif in_dims == self.m_dims and out_dims==self.s_dims:
                return self.imle.predict(x.flatten()).reshape(-1,1)
        else:
            return self.imle.to_gmm().inference(in_dims, out_dims, x).sample().T

    def update(self, m, s):
        self.imle.update(m.flatten(),s.flatten())

class ImleGmmModel(ImleModel):
    def update_gmm(self):
        self.gmm=self.imle.to_gmm()

    def infer(self, in_dims,out_dims,x):
        self.update_gmm()
        return self.gmm.inference(in_dims, out_dims, x).sample().T


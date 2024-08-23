"""
The code in this file is a part of q2nmr package, on which Eugene M. worked as a post-doctoral fellow at the
University of Canterbury from 2016 to 2021. The code has not been relesed publicly yet, but the following
give an example of numpy use within the package.

The q2nmr package solves the problem of model-based quantitative analysis of nuclear magnetic resonance (NMR) data.
The experimental NMR spectra are compared with the model signatures generated based on certain sets of parameters.
The parameter values that produce a model which fits the data the best determine the sought quantification results.
Solving the above problem requires extensive search over the parameter space and repeated evaluation of a non-
linear objective function.
"""

import numpy as np
import numexpr as ne

def arrhash(x):
    """Very quick and simple function to hash np arrays."""
    return x[0] + x[-1] + len(x)

class chemNode():
    """Base class that defines a model for a chemical species"""
    ...

class chemNodeQT(chemNode):
    """Model of chemical species evaluated based on the complete quantum mechanical formulation of the
    underlying spin system.
    """

    def __init__(self, name, chsh = None, alph = None, ampl = None, phase = None, intn = 1., alias=''):
        chemNode.__init__(self, name, chsh, alph, ampl, phase, intn, alias)
        self.qPoles = np.array([0.])
        self.qPolesIntn = 1.
        self.uPoles = 0.
        self.uF = []
        self.qT = []

    def default_pars(self):
        """Returns a dictionary of default parameters for the node."""
        return {'ampl':[self.ampl[0].dflt()], 'phase':[self.phase[0].dflt()]}

    def evalTime(self, t, **kwargs):
        """Computes the node's response sT in the time domain"""
        newHash = arrhash(t)

        if self.qT == [] or self._oldHash != newHash:
            self.qT = np.inner( np.exp(np.outer(t, self.qPoles)), self.qPolesIntn ).ravel()
        if self.sT == [] or self._oldHash != newHash:
            self.sT = self.intn * self.qT * np.exp(np.outer(t, self.sPole)).ravel()

        self._oldHash = newHash

    def propPoles(self, uPolePrnt = None):
        """Propagates offset poles to all children."""
        if uPolePrnt is None:
            uPolePrnt = 0. if self.isRoot() else self._parent.uPoles     # Set the offset pole to the uPole of the parent
        newPoles = self.sPole + uPolePrnt + self.qPoles
        if not np.array_equal(self.uPoles, newPoles):
            self.uPoles = 1j*newPoles.imag + np.minimum(newPoles.real, 0.0)
            self.uF = []    # Reset the output in the frequency domain

    def evalFreq(self, f, dt, df, c0, f0=0, tau=0):
        """Computes the node's response in the frequency domain assuming that all ancestors have updated uPoles."""
        # Check if the signal needs to be reevaluated
        newHash = arrhash(f)

        if len(self.uF) == 0 or self._oldHash != newHash:
            self.uF = np.exp(1j*tau*(self.uPoles.imag - 2*np.pi*f0)).reshape((1,-1))
            x1 = 1j*2*np.pi*(c0*f-f0).reshape((-1,1))
            x2 = np.conj(self.uPoles - 1j*2*np.pi*f0).reshape((1,-1))

            # self.uF = self.uF / -np.expm1((x1+x2)*dt)
            # self.uF = np.inner(np.conj(self.uF), self.qPolesIntn).ravel()

            self.uF = ne.evaluate( 'x / -expm1( (x1 + x2)*dt )', local_dict={'x':self.uF, 'x1':x1, 'x2':x2, 'dt':dt})       # Compute exp(x)-1 in one go
            self.uF = ne.evaluate('sum(conj( x ) * y, axis=1)', local_dict={'x':self.uF, 'y':self.qPolesIntn}).ravel()
            self.uF *= self.intn * np.sqrt(df*c0*dt)

            self._oldHash = newHash
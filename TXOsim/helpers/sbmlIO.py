# 2020 Nadanai Laohakunakorn
# Adapted from tellurium.py

from __future__ import print_function, division, absolute_import

import functools
import os
import sys
import warnings

# ---------------------------------------------------------------------
# Simple File Read and Store Utilities
# ---------------------------------------------------------------------
def saveToFile(filePath, str):
    """ Save string to file.
    see also: :func:`readFromFile`
    :param filePath: file path to save to
    :param str: string to save
    """
    with open(filePath, 'w') as f:
        f.write(str)


def readFromFile(filePath):
    """ Load a file and return contents as a string.
    see also: :func:`saveToFile`
    :param filePath: file path to read from
    :returns: string representation of the contents of the file
    """
    with open(filePath, 'r', encoding="utf8") as f:
        string = f.read()
    return string


def listFiles (wildcardstr):
    """ List the files names in the current directory using the wildcard argument
    
    eg te.listFiles ('*.xml')
    :param wildcardstr: WIld card using during the file search
    :returns: list of file names that match the wildcard
    """
    import glob
    return glob.glob (wildcardstr)

# ---------------------------------------------------------------------
# ODE extraction methods
# ---------------------------------------------------------------------        

def getODEsFromSBMLFile (fileName):
    """ Given a SBML file name, this function returns the model 
    as a string of rules and ODEs
    
    >>> te.getODEsFromSBMLFile ('mymodel.xml')
    """
    sbmlStr = readFromFile (fileName)
    extractor = ODEExtractor (sbmlStr)
    return extractor.toString()
    
def getODEsFromSBMLString (sbmlStr):
    """ Given a SBML string this fucntion returns the model 
    as a string of rules and ODEs
      
    >>> te.getODEsFromSBMLString (sbmlStr)
    """
    
    extractor = ODEExtractor (sbmlStr)
    return extractor.toString()
  
def getODEsFromModel (roadrunnerModel):
    """Given a roadrunner instance this function returns
    a string of rules and ODEs
    
    >>> r = te.loada ('S1 -> S2; k1*S1; k1=1')
    >>> te.getODEsFromModel (r)
    """       
    from roadrunner import RoadRunner
    if type (roadrunnerModel) == RoadRunner:
       extractor = ODEExtractor (roadrunnerModel.getSBML())
    else:
       raise RuntimeError('The argument to getODEsFromModel should be a roadrunner variable')
           
    return extractor.toString()
    
class Accumulator:
    def __init__(self, species_id):
        self.reaction_map = {}
        self.reactions = []
        self.species_id = species_id

    def addReaction(self, reaction, stoich):
        rid = reaction.getId()
        if rid in self.reaction_map:
            self.reaction_map[rid]['stoich'] += stoich
        else:
            self.reaction_map[rid] = {
                'reaction': reaction,
                'id': rid,
                'formula': self.getFormula(reaction),
                'stoich': stoich,
            }
            self.reactions.append(rid)

    def getFormula(self, reaction):
        return reaction.getKineticLaw().getFormula()

    def toString(self, use_ids=False):
        lhs = 'd{}/dt'.format(self.species_id)
        terms = []
        for rid in self.reactions:
            if abs(self.reaction_map[rid]['stoich']) == 1:
                stoich = ''
            else:
                stoich = str(abs(self.reaction_map[rid]['stoich'])) + '*'

            if len(terms) > 0:
                if self.reaction_map[rid]['stoich'] < 0:
                    op = ' - '
                else:
                    op = ' + '
            else:
                if self.reaction_map[rid]['stoich'] < 0:
                    op = '-'
                else:
                    op = ''

            if use_ids:
                expr = 'v' + self.reaction_map[rid]['id']
            else:
                expr = self.reaction_map[rid]['formula']

            terms.append(op + stoich + expr)

        rhs = ''.join(terms)
        return lhs + ' = ' + rhs

class ODEExtractor:
    def __init__(self, sbmlStr):
        try:
            import tesbml
        except ImportError:
            raise Exception("Cannot import tesbml. Try tellurium.installPackage('tesbml')")
            
        self.doc = tesbml.readSBMLFromString (sbmlStr)
        self.model = self.doc.getModel()
               
        self.species_map = {}
        self.species_symbol_map = {}
        self.use_species_names = False
        self.use_ids = True

        from collections import defaultdict
        self.accumulators = {}
        self.accumulator_list = []
      
        def reactionParticipant(participant, stoich):
            stoich_sign = 1
            if stoich < 0:
                stoich_sign = -1
            if participant.isSetStoichiometry():
                stoich = participant.getStoichiometry()
            elif participant.isSetStoichiometryMath():
                raise RuntimeError('Stoichiometry math not supported')
            self.accumulators[participant.getSpecies()].addReaction(r, stoich_sign*stoich)

        newReactant = lambda p: reactionParticipant(p, -1)      
        newProduct  = lambda p: reactionParticipant(p, 1)

        for s in (self.model.getSpecies(i) for i in range(self.model.getNumSpecies())):
            self.species_map[s.getId()] = s
            if s.isSetName() and self.use_species_names:
                self.species_symbol_map[s.getId()] = s.getName()
            else:
                self.species_symbol_map[s.getId()] = s.getId()
            a = Accumulator(s.getId())
            self.accumulators[s.getId()] = a
            self.accumulator_list.append(a)

        for r in (self.model.getReaction(i) for i in range(self.model.getNumReactions())):
            for reactant in (r.getReactant(i) for i in range(r.getNumReactants())):
                newReactant(reactant)
            for product in (r.getProduct(i) for i in range(r.getNumProducts())):
                newProduct(product)
        
    def getRules (self):
        r = ''
        for i in range (self.model.getNumRules()): 
            if self.model.getRule(i).getType() == 0:
                r += 'd' + self.model.getRule(i).id + '/dt = ' + self.model.getRule(i).formula + '\n'
            if self.model.getRule(i).getType() == 1:
                r += self.model.getRule(i).id + ' = ' + self.model.getRule(i).formula + '\n'
        return r
    
    def getKineticLaws (self):
        r = ''
        if self.use_ids:
            r += '\n'
            for rx in (self.model.getReaction(i) for i in range(self.model.getNumReactions())):           
                r += 'v' + rx.getId() + ' = ' + rx.getKineticLaw().getFormula().replace(" ", "")  + '\n'
        return r
    
    def getRateOfChange (self, index):
        return self.accumulator_list[index].toString(use_ids=self.use_ids) + '\n'
        
    def getRatesOfChange (self):
        r = '\n'
        for a in self.accumulator_list:
            r += a.toString(use_ids=self.use_ids) + '\n'
        return r
       
    def toString(self):
        r = self.getRules()  
        r = r + self.getKineticLaws() + '\n'
        for index in range (self.model.getNumSpecies()):
   #        if not self.model.getSpecies (index).boundary_condition: # Removed as attr doesn't exist
            r = r + self.getRateOfChange (index)     
        return r

# ---------------------------------------------------------------------
# ODE parser
# ---------------------------------------------------------------------

def parseODEs(r,odes):

    # Parsing of ODEs into cython code

    # Split odes into channels and derivatives (normally these separated by two spaces)
    parts = odes.split('\n\n')
    channels = parts[0].lstrip('\n').split('\n')
    derivs = parts[1].rstrip('\n').split('\n')

    channeldict = {}
    for channel in channels:
        channeldict[channel.split(' = ')[0]] = channel.split(' = ')[1]

    derivdict = {}
    for deriv in derivs:
        derivdict[deriv.split(' = ')[0]] = deriv.split(' = ')[1]

 #   print(derivdict) # print to debug
 #   print(channeldict)

    speciesIds = []
    derivatives = []
    for derivkey in derivdict.keys():
        speciesIds.append(derivkey[1:-3]) # Extract species ID from derivative string

        channelkey = derivdict[derivkey]

        # first get list of channels
        split = channelkey.split()
        channels = []
        for i in range(len(split)):
            if (split[i][0]!='+') & (split[i][0]!='-'):
                channels.append(split[i])
            elif (split[i][0]=='-') & (len(split[i])>1) :
                channels.append(split[i][1:])

        # then figure out their signs
        signs = []
        if (split[0][0]!='+') & (split[0][0]!='-'):
            signs.append('+')
        for i in range(len(split)):
            if split[i][0]=='-':
                signs.append('-')
            elif split[i][0]=='+':
                signs.append('+')
            elif (split[i]!='+') & (split[i]!='-'):
                pass

        derivatives.append(' '.join([signs[j]+' '+channeldict[channels[j]] for j in range(len(channels))]))

    speciesValues = r.getFloatingSpeciesConcentrations()
    parameterIds = r.getGlobalParameterIds()
    parameterValues = [value for value in r.getGlobalParameterValues()]

    return(speciesIds, speciesValues, parameterIds, parameterValues, derivatives)

# ---------------------------------------------------------------------
# Python code writer
# ---------------------------------------------------------------------

def writePython(speciesIds,speciesValues,parameterIds,parameterValues,derivatives,OUTPATH,FILENAME):
    # Generate cython script

    with open(OUTPATH+FILENAME,'w') as file:
        file.writelines('# Python model ODEs from antimony file\n\n')

        # Imports
        file.writelines('import numpy as np\n')
        file.writelines('\n')

        # Model definition
        file.writelines('def model(y, t, params):\n\n')

        # Species
        for i in range(len(speciesIds)):
            file.write('\t'+speciesIds[i]+' = y['+str(i)+']\n')

        file.writelines('\n')
        for i in range(len(parameterIds)):
            file.write('\t'+parameterIds[i]+' = params['+str(i)+']\n')

        file.writelines('\n')
        file.writelines('\tderivs = [\n')
        for i in range(len(derivatives)-1):
            file.write('\t'+derivatives[i]+',\n')
        file.write('\t'+derivatives[len(derivatives)-1]+']\n')

        file.write('\treturn derivs\n')


    file.close()
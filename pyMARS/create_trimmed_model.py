# Local Imports
import cantera as ct
import os

def trim(solution_object, exclusion_list, file_name):

    """ Function to reduce list of species and corresponding reactions.

    Arguments

    data_file:
        local .cti or .xml data file containing mechanism information
    exclusion_list:
        List of species that will be trimmed
    ----------
    Returns
        Original Cantera Solution Object
        Trimmed Cantera Solution Object
    ----------
    Example
        trim('gri30.cti', ['OH', 'H'])
        or
        trim('gri30.cti', []) to trim no species
    """
    print('species to exclude: ')
    print(exclusion_list)
    print ('\n')

    # define initial solution objects
    initial_solution = solution_object

    initial_species_objects = initial_solution.species
    initial_species_names = initial_solution.species_names

    initial_reaction_list = initial_solution.reactions()
    initial_reaction_objects = initial_solution.reactions

    # Remove reactions
    final_reaction_objects=[]
    for i, reaction in enumerate(initial_reaction_list):
        reaction_species = reaction.products.keys() + reaction.reactants.keys()
        difference = set(reaction_species).intersection(exclusion_list)
        if len(difference) == 0:
            final_reaction_objects.append(reaction)

    final_T=initial_solution.T
    final_P=initial_solution.P

    # Remove Species
    final_species_names=initial_species_names
    for n in exclusion_list:
        if n in initial_species_names:
            final_species_names.remove(n)

    final_species_objects =   [initial_solution.species(name) for name in final_species_names]

    # New solution definition
    new_solution= ct.Solution(  species=final_species_objects,
                                reactions=final_reaction_objects,
                                thermo='IdealGas',
                                kinetics='GasKinetics')
    new_solution.TP = initial_solution.TP
    new_solution.name = ('trimmed_' + os.path.splitext(file_name)[0])
    return (initial_solution, new_solution)

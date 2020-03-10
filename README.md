# ASReml-R
Tutorial on using ASReml-R in plant breeding experiments

## Dataset
The dataset we will be using for this tutorial will be 

## Expectations
The tutorial will help to understand and extract pertinent information related to breeding trials.

```
height ~ mu + site !r at(site).block family
```
Fits main effect of site as fixed, a random family effect and __at(site).block__ specifies a __unique variance__ component for __block at each site__: Y= u + site + block(site) + family + e, where family ~N(0,var_family) and block ~ N(0, var_block-sitei).
i.e. There is a diferent block variance for each site _i_.

```
height ~ mu + site !r at(site,1).block family
```
Fits the main effect of site as fixed, a random family effect and __at(site,1).block__ specifies a random block effect only within the _i_ th level of the site factor. In this example only at the first site.

```
at(Type, entry):GENOTYPE
```
Specifies a random GENOTYPE effect only within the _entry_ level of the factor _Type_.

## BLUP
For GWAS when Genotype is treated as a fixed effect
```
predict(asremlObject, classify='Genotype', maxiter=1)$pvals
```

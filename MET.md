## Analyzing multiple environment trials in ASREML-R


Input data

```
data_evaluate <- merged_appc_db %>% filter(Trait==Trt, Year==Yr, Species==Spc) %>% summarySE(measurevar = 'Value', groupvars=c("Year","Species","Site","Source","Entry","Rep"), na.rm = TRUE) %>% drop_na(Value)
```

Run model

```
model2c<-asreml(fixed=Value~Location+Rep+Location*Rep,
                  random=~corgh(Location):Entry,
                  residual=~dsum(~id(units)|Location),
                  data=data_evaluate, maxit=100000)
#update.asreml(model2c)
```

### Variance components
By default ```sigma``` parameterization is reported

```
summary(model2c)$varcomp
```

### BLUEs and BLUPs

```
summary(model2c,coef=TRUE)$coef.fixed # BLUEs # all=T is changed to coef=T in ASREML 4
summary(model2c,coef=TRUE)$coef.random # BLUPs
```

### Get predictions of genotypes across all sites

```
predict(model2c,classify="Entry")$pvals # prediction of genotype across sites
```

### Get prediction of genotypes for each site

```
predict(model2c,classify="Site:Entry")$pvals
```

### Wald's test for fixed effects

```
wald(model2c)
#or
wald.asreml(model2c)
```
### Heritability 

```
herit <-  vpredict(model2c,H2~V1/(V1+V2) # Change V based on variance component for each location
```

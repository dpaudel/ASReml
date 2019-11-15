## Analyzing multiple environment trials in ASREML-R


Input data

```
data_evaluate <- merged_appc_db %>% filter(Trait==Trt, Year==Yr, Species==Spc) %>% summarySE(measurevar = 'Value', groupvars=c("Year","Species","Site","Source","Entry","Rep"), na.rm = TRUE) %>% drop_na(Value)
```

Run model

```
 model2c<-asreml(fixed=Value~Site+Site:Rep,
                  random=~corgh(Site):Entry,
                  residual=~dsum(~id(units)|Site),
                  data=data_evaluate)
  #update.asreml(model2c)
```

### BLUEs and BLUPs

```
summary(model2c,coef=TRUE)$coef.fixed # BLUEs # all=T is changed to coef=T in ASREML 4
summary(model2c,coef=TRUE)$coef.random # BLUPs
```

# Get predictions of genotypes across all sites

```
predict(model2c,classify="Entry")$pvals # prediction of genotype across sites
```

### Get prediction of genotypes for each site

```
predict(model2c,classify="Site:Entry")$pvals
```

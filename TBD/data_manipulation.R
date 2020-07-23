library(dplyr)
library(stringr)
library(readr)

attach(zoo2MainSpecz)

str(zoo2MainSpecz)

# vamos a quedarnos con las variables y las clases de las primeras tres
# primero nos quedamos con las que sea True para la clase 1 (smooth)
cat1.smooth = zoo2MainSpecz %>% 
  select(names(zoo2MainSpecz)[1:4], names(zoo2MainSpecz)[str_detect(names(zoo2MainSpecz), 'a01')], names(zoo2MainSpecz)[str_detect(names(zoo2MainSpecz), 'a02')]) %>%
  filter(t01_smooth_or_features_a01_smooth_flag == 1) # 27k componentes

# primero nos quedamos con las que sea True para la clase 2 (features or disk)
cat2.disk.feature = zoo2MainSpecz %>% 
  select(names(zoo2MainSpecz)[1:4],names(zoo2MainSpecz)[str_detect(names(zoo2MainSpecz), 'a01')], names(zoo2MainSpecz)[str_detect(names(zoo2MainSpecz), 'a02')]) %>%
  filter(t01_smooth_or_features_a02_features_or_disk_flag == 1) # 79k componentes

# primero nos quedamos con las que sea True para la clase 3 (star or artifact)
# cat3.artifact.star = zoo2MainSpecz %>% 
#   select(names(zoo2MainSpecz)[1:4],names(zoo2MainSpecz)[str_detect(names(zoo2MainSpecz), 'a03')]) %>%
#   filter(t01_smooth_or_features_a03_star_or_artifact_flag == 1) # 30 componentes

# ahora los unimos en un unico dataset
dataset.cat1.cat2 = rbind(cat1.smooth, cat2.disk.feature)

dataset.cat1.cat2 %>% 
  select(t01_smooth_or_features_a01_smooth_flag) %>%
  filter(t01_smooth_or_features_a01_smooth_flag == 1) # comprobamos que haya unido bien

# vamos a crear la columna target
dataset.cat1.cat2$target = ifelse(dataset.cat1.cat2$t01_smooth_or_features_a01_smooth_flag == 1, 0, 1)
dataset.cat1.cat2$target

# me cargo las variables que no sirven
dataset.cat1.cat2$t01_smooth_or_features_a01_smooth_flag = NULL
dataset.cat1.cat2$t01_smooth_or_features_a02_features_or_disk_flag = NULL
dataset.cat1.cat2$specobjid = NULL
dataset.cat1.cat2$dr8objid = NULL
dataset.cat1.cat2$dr7objid = NULL
dataset.cat1.cat2$ra = NULL
dataset.cat1.cat2
sum(dataset.cat1.cat2[1:55000,]$target == 1)
write_csv(dataset.cat1.cat2[1:55000,], 'dataset_competition_IBM.csv')

names(dataset.cat1.cat2)

#!/usr/bin/R

# Solving the issue of admin0 and admin1 missing records.

library(dplyr)

csv_path = "config/dbo_GRF_AdminUnits.csv"

CreateUniqueAdmRecords = function(p) {
  data <- read.csv(p)
  cat("Data loaded with ", nrow(data), " records.\n")

  cat("Processing data...")

  # Admin1 Codes.
  adm1 <- data %>% distinct(ADM0_CODE, ADM1_CODE)
  adm1$ADM2_CODE <- NA
  adm1$ADM2_NAME <- NA

  # Admin0 Codes.
  adm0 <- data %>%
    distinct(ADM0_CODE)
  adm0$ADM1_CODE <- NA
  adm0$ADM1_NAME <- NA
  adm0$ADM2_CODE <- NA
  adm0$ADM2_NAME <- NA

  cat('done.\n')

  output <- rbind(data,adm1,adm0)

  # Converting NA to Null.
  # variables = c("ADM1_CODE", "ADM1_NAME", "ADM2_CODE", "ADM2_NAME")
  # for (i in 1:length(variables)) {
  #   output[variables[i]] <- ifelse(is.na(output[variables[i]]) == TRUE, NULL, output[variables[i]])
  # }

  return(output)
}

added_df <- CreateUniqueAdmRecords('config/dbo_GRF_AdminUnits.csv')
write.csv(added_df, "config/modified_admin_units.csv", row.names=F, na="", fileEncoding="UTF-8", quote=FALSE)

library(httr)
library(future)
library(furrr)
library(modelsummary)
library(readr)

# read comids
c <- read_csv("comid.zip")


# make API call URLs
api <- "https://merit.internetofwater.app/processes/river-runner/execution"
urls <- paste0(api,"?id=",c(1:2938143))


## API summarize results function
get_path <- function(url){
  resp <- httr::GET(url)
  url = resp$url
  time_seconds = resp$times["total"]
  status = as.character(resp$status_code)
  cache = resp$headers$`x-cache`
  return(data.frame(url,time_seconds,status,cache))
}

# paralellize and log results
cores <- future::availableCores() - 1 
plan(multisession,workers=cores)

log <- furrr::future_map_dfr(urls[1:10],get_path,.progress=TRUE)


# with_progress({
#   p <- progressor(steps = 1000)
# log <-furrr::future_map_dfr(urls[1:10000],~{
#   p()
#   get_path(.)
#   })
# })
write.csv(log,"cache_log.csv")

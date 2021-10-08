library(httr)
library(future)
library(furrr)

# read coordinates that are on land
coords <- read.csv("coords.csv")
api <- "https://merit.internetofwater.app/processes/river-runner/execution"

# remove Antarctica
coords2 <- coords[which(coords$Y>-56),]

# make API call URLs
urls <- paste0(api,"?lat=",coords2$Y,"&lng=",coords2$X)
urls <- na.omit(urls)

# make log data frame
log <- as.data.frame(cbind(urls,NA,NA))
names(log) <- c("urls","time","status")

## API summarize results function
get_path <- function(url){
  resp <- httr::GET(url)
  url = resp$url
  time_seconds = resp$times["total"]
  status = resp$status_code
  cache = resp$headers$`x-cache`
  return(data.frame(url,time_seconds,status,cache))
}

# paralellize and log results
cores <- future::availableCores() - 1 
plan(multisession,workers=cores)
log <-furrr::future_map_dfr(urls[1:100],get_path,.progress=TRUE)

write.csv(log,"cache_log.csv")

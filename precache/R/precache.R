library(httr)
library(future)
library(furrr)
library(modelsummary)
library(readr)
library(crul)

# read comids
c <- read_csv("comid.zip")


# make API call URLs
# make API call URLs
api <- "https://merit-nldi.internetofwater.app/processes/river-runner/execution"
api2 <- "https://merit-dev-z3iqgg3uaa-uc.a.run.app/processes/river-runner/execution"
urls <- paste0(api,"?id=",c(1:2938143))
urls2 <- paste0(api2,"?id=",c(1:2938143))

## API summarize results function
get_path <- function(url){
  resp <- httr::GET(url)
  url = resp$url
  time_seconds = resp$times["total"]
  status = as.character(resp$status_code)
#  cache = resp$headers$`x-cache`
  return(data.frame(url,time_seconds,status))
}

# paralellize and log results
cores <- future::availableCores() - 1 
plan(multisession,workers=cores)

sample <- sample.int(2938143,500)


system.time(log.bg <- furrr::future_map_dfr(urls[sample],get_path,.progress=TRUE))
system.time(log.sm <- furrr::future_map_dfr(urls2[sample],get_path,.progress=TRUE))


# asynchronous versiosn
u.b<- paste0(api,"?id=",c(1:2938143))
u.s <- paste0(api2,"?id=",c(1:2938143))

sample <- sample.int(2938143,100)
(big <- Async$new(
  urls = u.b[sample]
))

(small <- Async$new(
  urls = u.s[sample]
))


system.time(req.bg <- big$get())
system.time(req.sm <- small$get())
# with_progress({
#   p <- progressor(steps = 1000)
# log <-furrr::future_map_dfr(urls[1:10000],~{
#   p()
#   get_path(.)
#   })
# })
write.csv(log,"cache_log.csv")

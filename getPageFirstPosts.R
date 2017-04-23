library(plyr)
library(devtools)
library(reshape2)
library(igraph)
library(Rfacebook)
library(ggplot2)
library(GGally)
library(scales)
library(formattable)

#get permanent token for Facebook apps using variables from https://developers.facebook.com/apps
fbOauth <- fbOAuth(YOUR_KEY_HERE, YOUR_SECRET_HERE, extended_permissions = FALSE, legacy_permissions = FALSE)

## convert Facebook date format to R date format
format.facebook.date <- function(datestring) {
  date <- as.POSIXct(datestring, format = "%Y-%m-%dT%H:%M:%S+0000",tz = "GMT")
}

#search all pages
allPages <-searchPages('soldiers-of-odin', fbOauth, n=10000)
allPageIds <- allPages$id

#get posts of all pages without reactions
get.all.pages <- function(id) {
  page <- getPage(id, fbOauth, n = 5000, reactions = FALSE)
  #posts <- page$posts
}

#Get all pages, including posts, after searching their ids
allPosts <- mapply(get.all.pages, allPageIds, MoreArgs = NULL, USE.NAMES = TRUE)

## Aggregate all likes to create metric for counting page size
aggregate.likes <- function(likes_count) {
  likes <- sum(likes_count)
  return(likes)
}

## First posts of page
col_headings <- c('id','created', 'name')
firstPosts <- data.frame(id = character(0), created = character(0), name = character(0), total_likes = integer(0))
names(firstPosts) <- col_headings
for(i in names(allPosts)){
  name <-allPosts[[i]]$from_name[1]
  if (is.null(name)) { 
    name <- "-"
  }
  print(name)
  created_time <-(tail((allPosts[[i]]$created_time), n=1))
  if (is.null(created_time)) { 
    created_time <- "-"
  }
  print(created_time)
  total_likes <-sum(allPosts[[i]]$likes_count)
  firstPosts <- rbind(firstPosts,data.frame(i, name, created_time, total_likes))
}
print(firstPosts)

# Create data frame with month of firstpost
firstPosts$datetime <- format.facebook.date(firstPosts$created_time)
firstPosts$month <- format(firstPosts$datetime, "%Y-%m")
firstPosts.freqMonths <- as.data.frame(table(firstPosts$month))

## Plot frequency of new groups per month based on first post
frequency <-ggplot(firstPosts.freqMonths, aes(x=Var1, y=Freq), label=Var1) + geom_point(size=4, colour="blue")
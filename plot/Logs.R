library(stringr)

library(gridExtra)
log_pathes <- c( "/home/shuzhe/Simulations/Logs/default_log"      ,    "/home/shuzhe/Simulations/Logs/archive/22-23week"   ,
           "/home/shuzhe/Simulations/Logs/archive/20-21week" ,   "/home/shuzhe/Simulations/Logs/archive/19week"      ,
           "/home/shuzhe/Simulations/Logs/archive/prior_Feb"  ,  "/home/shuzhe/Simulations/Logs/archive/obsolete_log")

logs <-lapply(log_pathes, read.csv, sep = "\t")

total = Reduce(function(...) merge(..., all=T), logs)




write.csv(total, "/home/shuzhe/Simulations/Scripts/logs.csv", row.names = F)



a <- ggplot(total[total$Status == "F", ]) + geom_histogram(aes(x = month),stat="count") + theme_Publication() + scale_fill_Publication() + scale_colour_Publication() + labs(title = "Number of Jobs Submitted per Month")


b <- ggplot(total[total$Status == "F" &  ! is.na(total$cx) , ])  + theme_Publication() + scale_fill_Publication() + scale_colour_Publication()  + geom_histogram(aes(x = cx), stat = "count") + labs(title = "Jobs Submitted onto CX1 or CX2")


c <- ggplot(total[total$Status == "F" & (str_detect(total$cpus, "16") |str_detect(total$cpus, "1") | str_detect(total$cpus, "12") | str_detect(total$cpus, "20") )& total$cpus != "11" &  ! is.na(total$cpus), ])  + theme_Publication() + scale_fill_Publication() + scale_colour_Publication()  + geom_histogram(aes(x = cpus), stat = "count") + labs(title = "Jobs Submitted onto Different Queues on CX1")



png(file=str_c("/home/shuzhe/Simulations/Figures/logs_stats.png"),width = 12, height = 8, units = 'in', res = 300)
grid.arrange(a,b,c, layout_matrix = matrix(c(1,2,1,3), nrow =2))
dev.off()
overall

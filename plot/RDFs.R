plot_rdf <- function(ldf){
    theme_Publication <- function(base_size=14, base_family="helvetica") {
        library(grid)
        library(ggthemes)
        (theme_foundation(base_size=base_size, base_family=base_family)
            + theme(plot.title = element_text(face = "bold",
                                              size = rel(1.2), hjust = 0.5),
                    text = element_text(),
                    panel.background = element_rect(colour = NA),
                    plot.background = element_rect(colour = NA),
                    panel.border = element_rect(colour = NA),
                    axis.title = element_text(face = "bold",size = rel(1)),
                    axis.title.y = element_text(angle=90,vjust =2),
                    axis.title.x = element_text(vjust = -0.2),
                    axis.text = element_text(), 
                    axis.line = element_line(colour="black"),
                    axis.ticks = element_line(),
                    panel.grid.major = element_line(colour="#f0f0f0"),
                    panel.grid.minor = element_blank(),
                    legend.key = element_rect(colour = NA),
                    legend.position = "none",
                    legend.direction = "horizontal",
                    legend.key.size= unit(0.5, "cm"),
                    legend.margin = unit(0, "cm"),
                    legend.title = element_text(face="italic"),
                    plot.margin=unit(c(10,5,5,5),"mm"),
                    strip.background=element_rect(colour="#f0f0f0",fill="#f0f0f0"),
                    strip.text = element_text(face="bold")
            ))
        
    }

    out <- list()
    # for(i in 1:length(ldf))
    #     out[[i]] <- ggplot(ldf[[i]], aes(x = distance , y = rdf)) + geom_line(aes(color = time)) + facet_grid(time ~ ., scales = "free") + theme_Publication() + labs(title = str_c(names(ldf)[i], ": Radial Distribution Function of Water Around Hydroxylate Group"),              x = "r (nm)" ,                   y = "g(r)")
    #     
    
    for(i in 1:length(ldf))
        out[[i]] <- ggplot(ldf[[i]], aes(x = distance , y = rdf)) + geom_line()  + theme_Publication() + labs(title = str_c(names(ldf)[i], ": Radial Distribution Function of Water Around Hydroxylate Group"),              x = "r (nm)" ,                   y = "g(r)") + scale_colour_Publication() + theme_Publication() + scale_y_continuous(trans = "log")
        
    return(out)    
}
#####################################################
rdf_pathes <- c( "/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/rdf.csv" ,
                 "/home/shuzhe/Simulations/22week/9.MA1x5_solv_with_buffer/Output/rdf.csv" ,
                 "/home/shuzhe/Simulations/22week/10.MB0x5_solv_with_buffer/Output/rdf.csv",
                 "/home/shuzhe/Simulations/22week/11.MB1x5_solv_with_buffer/Output/rdf.csv")

rdfs <- lapply(rdf_pathes, read.csv)
for(i in 1:length(rdfs)) {
    rdfs[[i]] <- rdfs[[i]][rdfs[[i]]$time != 0 , ]
    rdfs[[i]]$distance <- rdfs[[i]]$distance * 0.1
    rdfs[[i]]$time <- str_c(as.character(rdfs[[i]]$time * 0.01 ), " ns")
    
}
names(rdfs) <- c("AAAAA(0)", "AAAAA(1)", "BBBBB(0)", "BBBBB(1)")

counter = 1
for(i in plot_rdf(rdfs)) {
    # png(file=str_c("/home/shuzhe/Simulations/Figures/rdfs/", names(rdfs)[counter], "rdf.png"),width = 10, height = 8, units = 'in', res = 300)
    print(i)
    # dev.off()
    counter <- counter + 1
}            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
############################3
theme_Publication <- function(base_size=14, base_family="helvetica") {
    library(grid)
    library(ggthemes)
    (theme_foundation(base_size=base_size, base_family=base_family)
        + theme(plot.title = element_text(face = "bold",
                                          size = rel(1.2), hjust = 0.5),
                text = element_text(),
                panel.background = element_rect(colour = NA),
                plot.background = element_rect(colour = NA),
                panel.border = element_rect(colour = NA),
                axis.title = element_text(face = "bold",size = rel(2)),
                axis.title.y = element_text(angle=90,vjust =2, size = 20),
                axis.title.x = element_text(vjust = -0.2, size = 20),
                axis.text = element_text(size = 15), 
                axis.line = element_line(colour="black"),
                axis.ticks = element_line(),
                panel.grid.major = element_line(colour="#f0f0f0"),
                panel.grid.minor = element_blank(),
                legend.key = element_rect(colour = NA),
                legend.position = "bottom",
                legend.direction = "horizontal",
                legend.key.size= unit(1, "cm"),
                legend.margin = unit(0, "cm"),
                legend.title = element_blank(),
                plot.margin=unit(c(10,5,5,5),"mm"),
                strip.background=element_rect(colour="#f0f0f0",fill="#f0f0f0"),
                strip.text = element_text(face="bold")
        ))
    
}
plot_rdf_single <- function(df){
    # order = rep(names(rdfs), each = 200)
    df$type <-  factor(df$type, levels = c("AAAAA(0)",  "BBBBB(0)", "AAAAA(1)","BBBBB(1)"))
    g <- ggplot(df, aes(x = distance , y = rdf)) + geom_line(size = 1.1, aes(color = type)) + facet_grid(type ~ ., scales = "free") + theme_Publication() + labs(title = str_c( "Radial Distribution Function of Water Around Hydroxylate Group"),              x = "r (nm)" ,                   y = "g(r)")

    
    # for(i in 1:length(ldf))
    #     out[[i]] <- ggplot(ldf[[i]], aes(x = distance , y = rdf)) + geom_line()  + theme_Publication() + labs(title = str_c(names(ldf)[i], ": Radial Distribution Function of Water Around Hydroxylate Group"),              x = "r (nm)" ,                   y = "g(r)") + scale_colour_Publication() + theme_Publication() + scale_y_continuous(trans = "log")
    # 
    return(g)    
}

rdf_pathes <- c( "/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/rdf.csv" ,
                 "/home/shuzhe/Simulations/22week/10.MB0x5_solv_with_buffer/Output/rdf.csv",
                 "/home/shuzhe/Simulations/22week/9.MA1x5_solv_with_buffer/Output/rdf.csv" ,
                 "/home/shuzhe/Simulations/22week/11.MB1x5_solv_with_buffer/Output/rdf.csv")

rdfs <- lapply(rdf_pathes, read.csv)
names(rdfs) <- c("AAAAA(0)",  "BBBBB(0)", "AAAAA(1)","BBBBB(1)")
df <- rdfs[[1]][rdfs[[1]]$time == 6000, ]
df$type <- names(rdfs)[1]
for(i in 2:length(rdfs)){
    tmp <- rdfs[[i]][rdfs[[i]]$time == 6000, ]
    tmp$type <- names(rdfs)[i]
    df <- rbind(df, tmp)
}


levels(df$type) <- c("AAAAA(0)",  "BBBBB(0)", "AAAAA(1)","BBBBB(1)")
scale_colour_Publication <- function(...){
    library(scales)
    discrete_scale("colour","Publication",manual_pal(values = c("#386cb0","#7fc97f","#fdb462","#ef3b2c","#662506","#a6cee3","#fb9a99","#984ea3","#ffff33")), ...)
}

png(file=str_c("/home/shuzhe/Simulations/Figures/rdfs.png"),width = 12, height = 8, units = 'in', res = 300)
plot_rdf_single(df)+ scale_colour_Publication() + theme_Publication() 
dev.off()
























##################################
rdf_pathes <- c( "/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/rdf_water.csv" ,
                 "/home/shuzhe/Simulations/22week/9.MA1x5_solv_with_buffer/Output/rdf_water.csv" ,
                 "/home/shuzhe/Simulations/22week/10.MB0x5_solv_with_buffer/Output/rdf_water.csv",
                 "/home/shuzhe/Simulations/22week/11.MB1x5_solv_with_buffer/Output/rdf_water.csv")


rdfs <- lapply(rdf_pathes, read.csv)
names(rdfs) <- c("AAAAA(0)", "AAAAA(1)", "BBBBB(0)", "BBBBB(1)")
df <- rdfs[[1]]
df$type <- names(rdfs)[1]
for(i in 2:length(rdfs)){
    tmp <- rdfs[[2]]
    tmp$type <- names(rdfs)[2]
    df <- rbind(df, tmp)
}
plot_rdf_single(df)

counter = 1
for(i in plot_rdf(rdfs)) {
    png(file=str_c("/home/shuzhe/Simulations/Figures/rdfs/", names(rdfs)[counter], "water_rdf.png"),width = 10, height = 8, units = 'in', res = 300)
    print(i)
    dev.off()
    counter <- counter + 1
}            

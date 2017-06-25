plot_pmf_error <- function(list_df){
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
                    legend.position = "bottom",
                    legend.text =  element_text(size = 50000),
                    legend.direction = "horizontal",
                    # legend.key.size= unit(2.5, "cm"),
                    legend.margin = unit(0, "cm"),
                    legend.title = element_text(face="italic", size = 100),
                    plot.margin=unit(c(10,5,5,5),"mm"),
                    strip.background=element_rect(colour="#f0f0f0",fill="#f0f0f0"),
                    strip.text = element_text(face="bold")
            )) 
        
    }
    
    scale_fill_Publication <- function(...){
        library(scales)
        discrete_scale("fill","Publication",manual_pal(values = c("#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99","#984ea3","#ffff33")), ...)
        
    }
    
    scale_colour_Publication <- function(...){
        library(scales)
        discrete_scale("colour","Publication",manual_pal(values = c("#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99","#984ea3","#ffff33")), ...)
        
    }
    
    
    colors <- brewer.pal(length(list_df), "Set1")
    names(colors) <- names(list_df)
    print(colors)
    counter = 1
    g <- "ggplot()"
    for(i in 1:length(list_df)){
        g <- str_c(g , " + geom_line(data = list_df[[", i, "]], aes(color = names(list_df)[", i, "], x = list_df[[" , i, "]][, 1], y = list_df[[", i, "]][, 2]), size = 1.25) ")
        print(g)
        counter <- counter + 1
    }
    g <- str_c(g , " + scale_fill_brewer()")
    g <- eval(parse(text = g))
    g <- g + 
        labs(#title = "Potential of Mean Force Comparisons",
            x = "Distance of Separation (nm)" , 
            y = "Free Energy (kJ/mol)") + 
        theme(plot.title = element_text(hjust = 0.5))
    g <- g + theme_Publication() + scale_colour_Publication() +
        scale_colour_manual( name = "", values=colors) 
    return(g)    
}


read.xvg <- function(path, sep = "\t", header = F) {
    df <- readLines(path)
    skip <- max(which(str_detect(df, "^[@|#]")))
    read.table(path, skip = skip, sep = "" , header = F ,               na.strings ="", stringsAsFactors= F)
    
    }

polymer_pathes <- c( "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/Output_frame1/msd.xvg"     ,
                     "/home/shuzhe/Simulations/25week/10.MA1x5_US/Output_frame1/msd.xvg"           ,  
                     "/home/shuzhe/Simulations/25week/1.MB0x5_DPPC_US_ion/Output_frame3/msd.xvg"  ,   
                     "/home/shuzhe/Simulations/25week/11.MB1x5_US/Output_frame2/msd.xvg"             )

polymers <- lapply(polymer_pathes, read.xvg)
names(polymers) <- c("AAAAA(0)", "AAAAA(1)","BBBBB(0)",  "BBBBB(1)")
plot_pmf_error(polymers)+ scale_colour_Publication() + theme_Publication()+ labs( y = bquote(bold('Mean Square Displacement ('~nm^2~')')) ,     x = "Time (ps)") + xlim(0, 10000) + ylim(0,4)

polymer_pathes <- c( "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/Output_frame21/msd.xvg"     ,
                     "/home/shuzhe/Simulations/25week/10.MA1x5_US/Output_frame39/msd.xvg"           ,  
                     "/home/shuzhe/Simulations/25week/1.MB0x5_DPPC_US_ion/Output_frame24/msd.xvg"  ,   
                     "/home/shuzhe/Simulations/25week/11.MB1x5_US/Output_frame51/msd.xvg"             )

polymers <- lapply(polymer_pathes, read.xvg)
names(polymers) <- c("AAAAA(0)", "AAAAA(1)","BBBBB(0)",  "BBBBB(1)")
plot_pmf_error(polymers)+ scale_colour_Publication() + theme_Publication()+ labs( y = bquote(bold('Mean Square Displacement ('~nm^2~')')) ,     x = "Time (ps)") + xlim(0, 10000) + ylim(0,4)


polymer_pathes <- c( "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/Output_frame43/msd.xvg"     ,
                     "/home/shuzhe/Simulations/25week/10.MA1x5_US/Output_frame83/msd.xvg"           ,  
                     "/home/shuzhe/Simulations/25week/1.MB0x5_DPPC_US_ion/Output_frame47/msd.xvg"  ,   
                     "/home/shuzhe/Simulations/25week/11.MB1x5_US/Output_frame100/msd.xvg"             )

polymers <- lapply(polymer_pathes, read.xvg)
names(polymers) <- c("AAAAA(0)", "AAAAA(1)","BBBBB(0)",  "BBBBB(1)")
plot_pmf_error(polymers)+ scale_colour_Publication() + theme_Publication() + labs( y = bquote(bold('Mean Square Displacement ('~nm^2~')')) ,     x = "Time (ps)") + xlim(0, 10000) + ylim(0,4)


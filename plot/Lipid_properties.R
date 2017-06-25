polymer_pathes <- c("/home/shuzhe/Simulations/MA0_thickness.csv", "/home/shuzhe/Simulations/MA1_thickness.csv",
                     "/home/shuzhe/Simulations/MB0_thickness.csv" ,"/home/shuzhe/Simulations/MB1_thickness.csv")

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
                    legend.direction = "horizontal",
                    legend.key.size= unit(0.5, "cm"),
                    legend.margin = unit(0, "cm"),
                    legend.title = element_text(face="italic"),
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
        g <- str_c(g , " + geom_ribbon(data = list_df[[", i, "]], aes(x = list_df[[", i, "]][,1], ymin = list_df[[", i, "]][,2] - list_df[[", i, "]][,3], ymax = list_df[[", i, "]][,2] + list_df[[", i, "]][,3]), fill = 'grey70', alpha = 0.5) ", " + geom_line(data = list_df[[", i, "]], aes(color = names(list_df)[", i, "], x = list_df[[" , i, "]][, 1], y = list_df[[", i, "]][, 2]), size = 1.25) ")
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

polymers <- lapply(polymer_pathes, read.csv)
names(polymers) <- c("AAAAA(0)", "AAAAA(1)",  "BBBBB(0)", "BBBBB(1)")
plot_pmf_error(polymers)+ scale_colour_Publication() + theme_Publication() + labs( x = "Distance of Separation (nm)" ,     y = "DPPC Thickness (nm)") + xlim(-4, 0)

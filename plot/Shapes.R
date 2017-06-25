
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
                axis.title.y = element_text(angle=90,vjust =2, size = 15),
                axis.title.x = element_text(vjust = -0.2, size = 15),
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


scale_colour_Publication <- function(...){
    library(scales)
    discrete_scale("colour","Publication",manual_pal(values = c("#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99","#984ea3","#ffff33")), ...)
    
}
# ggplot(df) + geom_density(aes(x=A0))+ geom_density(aes(x=A1))+ geom_density(aes(x=B0))+ geom_density(aes(x=B1)) + theme_Publication() + scale_fill_Publication() + scale_colour_Publication()



path <- "/home/shuzhe/Simulations/Figures/gyration.csv"
df <- read.csv(path)
x <- c(df$A0, df$A1, df$B0, df$B1)
names <- c(rep("AAAAA(0)",100), rep("AAAAA(-)", 100), rep("BBBBB(0)",100), rep("BBBBB(-)",100))
df <- data.frame(val = x/10, names = factor(names))

png(file=str_c("/home/shuzhe/Simulations/Figures/gyrations.png"),width = 10, height = 8, units = 'in', res = 300)
g <- ggplot(df) + geom_density(aes(x=val, colour = names, y=..density..), size = 1.1)+ theme_Publication() + scale_fill_Publication() + scale_colour_Publication() + xlim(0.5,1) + theme(legend.title=element_blank()) + labs(title = "Radius of Gyrations for Most Stable State of Each Polymer in Water", x = "Radius of gyration (nm)", y = "Probability density")
g
dev.off()

                                                                                                                                                             
                                                                                                                                                             
########################3

path <- "/home/shuzhe/Simulations/Figures/gyration_interface.csv"
df <- read.csv(path)
x <- c(df$A0, df$A1, df$B0, df$B1)
names <- c(rep("AAAAA(0)",100), rep("AAAAA(-)", 100), rep("BBBBB(0)",100), rep("BBBBB(-)",100))
df <- data.frame(val = x/10, names = factor(names))

png(file=str_c("/home/shuzhe/Simulations/Figures/gyrations_interface.png"),width = 10, height = 8, units = 'in', res = 300)
g <- ggplot(df) + geom_density(aes(x=val, colour = names, y=..density..), size = 1.1)+ theme_Publication() + scale_fill_Publication() + scale_colour_Publication() + xlim(0.5,1.5) + theme(legend.title=element_blank()) + labs(title = "Radius of Gyrations for Most Stable State of Each Polymer at Interface", x = "Radius of gyration (nm)", y = "Probability density")
g
dev.off()
####################################33

path <- "/home/shuzhe/Simulations/Figures/end2end.csv"
df <- read.csv(path)
x <- c(df$A0, df$A1, df$B0, df$B1)
names <- c(rep("AAAAA(0)",100), rep("AAAAA(-)", 100), rep("BBBBB(0)",100), rep("BBBBB(-)",100))
df <- data.frame(val = x/10, names = factor(names))
g <- ggplot(df) + geom_density(aes(x=val, colour = names, y=..count..), size=1.25)+ theme_Publication() + scale_fill_Publication() + scale_colour_Publication()  + theme(legend.title=element_blank()) + labs(title = "Radius of Gyrations for Most Stable State of Each Polymer", x = "Radius of gyration (nm)", y = "Probability density") + xlim()



g


########################################
path <- "/home/shuzhe/Simulations/Figures/end2end_interface.csv"
df <- read.csv(path)
x <- c(df$A0, df$A1, df$B0, df$B1)
names <- c(rep("AAAAA(0)",100), rep("AAAAA(-)", 100), rep("BBBBB(0)",100), rep("BBBBB(-)",100))
df <- data.frame(val = x/10, names = factor(names))
g <- ggplot(df) + geom_density(aes(x=val, colour = names, y=..count..))+ theme_Publication() + scale_fill_Publication() + scale_colour_Publication()  + theme(legend.title=element_blank()) + labs(title = "Radius of Gyrations for Most Stable State of Each Polymer", x = "Radius of gyration (nm)", y = "Probability density") 



g


library(gridExtra)
DPPC_HEADGROUP <- -2.0
DPPG_HEADGROUP <- -2.9
###################3

monomer_pathes <- c( "/home/shuzhe/Simulations/21week/15.MA0_DPPC_US/Analysis/bsResult.xvg",
                     "/home/shuzhe/Simulations/21week/16.MA1_DPPC_US/Analysis/bsResult.xvg",
                     "/home/shuzhe/Simulations/21week/17.MB0_DPPC_US/Analysis/bsResult.xvg",
                     "/home/shuzhe/Simulations/21week/18.MB1_DPPC_US/Analysis/bsResult.xvg")

monomers <- lapply(monomer_pathes, read.xvg)
monomers[[3]]$V1 <- -1 * monomers[[3]]$V1
monomers[[3]]$V2 <- monomers[[3]]$V2 - monomers[[3]]$V2[199]

names(monomers) <- c("A(0)", "A(1)", "B(0)", "B(1)")

plot_pmf_error(monomers) + xlim(-4, 0)+ geom_vline(xintercept = DPPC_HEADGROUP, alpha = 0.5)

png(file=str_c("/home/shuzhe/Simulations/Figures/monomer_pmf.png"),width = 10, height = 8, units = 'in', res = 300)
plot_pmf_error(monomers) + xlim(-4, 0)+ geom_vline(xintercept = DPPC_HEADGROUP, alpha = 0.5) + labs(title = "Potential of Mean Force Comparisons Between Monomers")+ scale_colour_Publication() + theme_Publication() 
dev.off()

# Free energy summary
for(i in monomers){
    i <- i[i$V1 <= 0, "V2" ]
    print(str_c(min(i)," ", max(i), " ", max(i) - min(i)))
}
#####################################33
polymer_pathes <- c( "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/Analysis/bsResult.xvg"     ,
                     "/home/shuzhe/Simulations/25week/1.MB0x5_DPPC_US_ion/Analysis/bsResult.xvg"  ,   
                     "/home/shuzhe/Simulations/25week/10.MA1x5_US/Analysis/bsResult.xvg"           ,  
                     "/home/shuzhe/Simulations/25week/11.MB1x5_US/Analysis/bsResult.xvg"            , 
                     "/home/shuzhe/Simulations/25week/22.MA0x2MB0MA0x2_DPPC_US/Analysis/bsResult.xvg",
                     "/home/shuzhe/Simulations/25week/23.MA1x2MB1MA1x2_DPPC_US/Analysis/bsResult.xvg",
                     "/home/shuzhe/Simulations/25week/24.MA0x4MB0_DPPC_US/Analysis/bsResult.xvg"     ,
                     "/home/shuzhe/Simulations/25week/25.MA1x4MB1_DPPC_US/Analysis/bsResult.xvg"   )

polymers <- lapply(polymer_pathes, read.xvg)
names(polymers) <- c("AAAAA(0)", "BBBBB(0)", "AAAAA(1)", "BBBBB(1)", "AABAA(0)", "AABAA(1)", "AAAAB(0)", "AAAAB(1)")

a <- plot_pmf_error(polymers) + xlim(-4,0) + geom_vline(xintercept = DPPC_HEADGROUP, alpha = 0.5)+ scale_colour_Publication() + theme_Publication() + 
b <- plot_pmf_error(polymers) + xlim(-4.2,-2) + ylim(-25, 25) + geom_hline(yintercept = -20, alpha = 0.5, linetype="dashed")+ scale_colour_Publication() + theme_Publication() 


png(file=str_c("/home/shuzhe/Simulations/Figures/polymer_pmf.png"),width = 17, height = 8, units = 'in', res = 300)
grid.arrange(a,b,top=textGrob("Potential of Mean Force Comparisons Between Polymers",gp=gpar(fontface="bold", fontsize = 30)), layout_matrix = matrix(c(1,2), ncol =2))
dev.off()

# Free energy summary
for(i in polymers){
    # i <- i[i$V1 <= 0, ]
    # print(summary(i))
    i <- i[i$V1 <= 0, "V2" ]
    print(str_c(min(i)," ", max(i), " ", max(i) - min(i)))
}


#####################################33
peptide_pathes <- c("/home/shuzhe/Simulations/25week/21.PEP_DPPC_US/Analysis/bsResult.xvg",
                    "/home/shuzhe/Simulations/26week/8.PEP_DPPG_US/Analysis/bsResult.xvg" )
peptides <- lapply(peptide_pathes, read.xvg)
names(peptides) <- c("DPPC", "DPPG")

png(file=str_c("/home/shuzhe/Simulations/Figures/peptide_pmf.png"),width = 17, height = 8, units = 'in', res = 300)
plot_pmf_error(peptides) + xlim(-4, 0) + geom_vline(xintercept = DPPC_HEADGROUP, alpha = 0.5, color = "red" ) + geom_vline(xintercept = DPPG_HEADGROUP, alpha = 0.5, color = "blue" ) + labs(title = "Potential of Mean Force Comparisons Between Different Bilayers")

dev.off()

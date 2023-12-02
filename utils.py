import math

SOL_OMUZ = 5
SAG_OMUZ = 6
SAG_BILEK = 16
SOL_BILEK = 15
SOL_BEL = 11
SAG_BEL = 12
SOL_DIRSEK = 7
SAG_DIRSEK = 8
SOL_EL = 9
SAG_EL = 10
SOL_DIZ = 13
SAG_DIZ = 14

def comelme_hesapla(sol_bilek,sol_diz,sol_bel,sag_bilek,sag_diz,sag_bel,sag_omuz,sol_omuz):
    try:
        #sol1 = math.dist(sol_bilek,sol_diz)
        #sol2 = math.dist(sol_diz,sol_bel)
        #sol3 = math.dist(sol_bel,sol_bilek)
        #aci_sol = math.degrees(math.acos((sol1*sol1+sol2*sol2-sol3*sol3)/(2*sol1*sol2)))
        #sag1 = math.dist(sag_bilek,sag_diz)
        #sag2 = math.dist(sag_diz,sag_bel)
        #sag3 = math.dist(sag_bel,sag_bilek)
        #aci_sag = math.degrees(math.acos((sag1*sag1+sag2*sag2-sag3*sag3)/(2*sag1*sag2)))
        sag_bel1 = math.dist(sag_omuz,sag_bel)
        sag_bel2 = math.dist(sag_bel,sag_diz)
        sag_bel3 = math.dist(sag_diz,sag_omuz)
        aci_sag_bel = math.degrees(math.acos((sag_bel1*sag_bel1+sag_bel2*sag_bel2-sag_bel3*sag_bel3)/(2*sag_bel1*sag_bel2)))
        sol_bel1 = math.dist(sol_omuz,sol_bel)
        sol_bel2 = math.dist(sol_bel,sol_diz)
        sol_bel3 = math.dist(sol_diz,sol_omuz)
        aci_sol_bel = math.degrees(math.acos((sol_bel1*sol_bel1+sol_bel2*sol_bel2-sol_bel3*sol_bel3)/(2*sol_bel1*sol_bel2)))
        if (aci_sag_bel<90 and aci_sol_bel<90):
            return True
        else:
            return False
    except ZeroDivisionError:
        pass

def yatma_hesapla(sol_dirsek,sol_omuz,sol_bel,sol_diz,sol_bilek,sag_dirsek,sag_omuz,sag_bel,sag_diz,sag_bilek):
    try:
        sol_omuz1 = math.dist(sol_dirsek,sol_omuz)
        sol_omuz2 = math.dist(sol_omuz,sol_bel)
        sol_omuz3 = math.dist(sol_bel,sol_dirsek)
        aci_sol_omuz = math.degrees(math.acos((sol_omuz1*sol_omuz1+sol_omuz2*sol_omuz2-sol_omuz3*sol_omuz3)/(2*sol_omuz1*sol_omuz2)))
        sag_omuz1 = math.dist(sag_dirsek,sag_omuz)
        sag_omuz2 = math.dist(sag_omuz,sag_bel)
        sag_omuz3 = math.dist(sag_bel,sag_dirsek)
        aci_sag_omuz = math.degrees(math.acos((sag_omuz1*sag_omuz1+sag_omuz2*sag_omuz2-sag_omuz3*sag_omuz3)/(2*sag_omuz1*sag_omuz2)))
        sol_bacak1 = math.dist(sol_bilek,sol_diz)
        sol_bacak2 = math.dist(sol_diz,sol_bel)
        sol_bacak3 = math.dist(sol_bel,sol_bilek)
        aci_sol_bacak = math.degrees(math.acos((sol_bacak1*sol_bacak1+sol_bacak2*sol_bacak2-sol_bacak3*sol_bacak3)/(2*sol_bacak1*sol_bacak2)))
        sag_bacak1 = math.dist(sag_bilek,sag_diz)
        sag_bacak2 = math.dist(sag_diz,sag_bel)
        sag_bacak3 = math.dist(sag_bel,sag_bilek)
        aci_sag_bacak = math.degrees(math.acos((sag_bacak1*sag_bacak1+sag_bacak2*sag_bacak2-sag_bacak3*sag_bacak3)/(2*sag_bacak1*sag_bacak2)))

        if (((aci_sol_omuz>30 and aci_sol_omuz<120) and (aci_sag_omuz<120 and aci_sag_omuz>30))) and (((aci_sag_bacak>90 and aci_sag_bacak<=180) and (aci_sol_bacak<=180 and aci_sag_bacak>90))):
            return True
        else:
            return False
    except ZeroDivisionError:
        pass

def kosma_hesapla(sol_el,sol_dirsek,sol_omuz,sag_el,sag_dirsek,sag_omuz,sol_bilek,sol_diz,sol_bel,sag_bilek,sag_diz,sag_bel):
    try:
        sol_el1 = math.dist(sol_el,sol_dirsek)
        sol_el2 = math.dist(sol_dirsek,sol_omuz)
        sol_el3 = math.dist(sol_omuz,sol_el)
        aci_sol_el = math.degrees(math.acos((sol_el1*sol_el1+sol_el2*sol_el2-sol_el3*sol_el3)/(2*sol_el1*sol_el2)))
        sag_el1 = math.dist(sag_el,sag_dirsek)
        sag_el2 = math.dist(sag_dirsek,sag_omuz)
        sag_el3 = math.dist(sag_omuz,sag_el)
        aci_sag_el = math.degrees(math.acos((sag_el1*sag_el1+sag_el2*sag_el2-sag_el3*sag_el3)/(2*sag_el1*sag_el2)))
        sag_bacak1 = math.dist(sag_bilek,sag_diz)
        sag_bacak2 = math.dist(sag_diz,sag_bel)
        sag_bacak3 = math.dist(sag_bel,sag_bilek)
        aci_sag_bacak = math.degrees(math.acos((sag_bacak1*sag_bacak1+sag_bacak2*sag_bacak2-sag_bacak3*sag_bacak3)/(2*sag_bacak1*sag_bacak2)))
        sol_bacak1 = math.dist(sol_bilek,sol_diz)
        sol_bacak2 = math.dist(sol_diz,sol_bel)
        sol_bacak3 = math.dist(sol_bel,sol_bilek)
        aci_sol_bacak = math.degrees(math.acos((sol_bacak1*sol_bacak1+sol_bacak2*sol_bacak2-sol_bacak3*sol_bacak3)/(2*sol_bacak1*sol_bacak2)))
        if (aci_sol_el<120 and aci_sag_el<120) and ((aci_sag_bacak>90 and aci_sag_bacak<180) or (aci_sol_bacak>90 and aci_sol_bacak<180)):
            return True
        else:
            return False
    except ZeroDivisionError:
        pass
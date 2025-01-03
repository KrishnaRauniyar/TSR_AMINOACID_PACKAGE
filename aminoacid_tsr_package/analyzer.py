import math
import pandas as pd
from .utils.theta_utils import thetaClass
from .utils.distance_utils import dist12Class

class AminoAcidAnalyzer:
    def __init__(self, dtheta, dLen, numOfLabels):
        self.dtheta = dtheta
        self.dLen = dLen
        self.numOfLabels = numOfLabels
        # These are the different labels of the atoms with their unique code (From CSV File)
        self.aminoAcidLabelWithCode = {}
        # Store animo acids code, x coordinate, y coordinate, z coordinate
        self.aminoAcidCode = {}
        self.xCoordinate = {}
        self.yCoordinate = {}
        self.zCoordinate = {}
        # This is to store the sequence number
        self.aminoSeqNum = {}
        # These three holds the label code of three amino acid, sorted them, and then store the sorted index 
        self.initAminoLabel = [0, 0, 0]
        self.sortedAminoLabel = [0, 0, 0]
        self.sortedAminoIndex = [0, 0, 0]
        # keys with its frequency
        self.keyFreq = {}
        # totak number of keys, and max distance list
        self.totalKeys = []
        self.maxDistList = []
        # This is reading the csv file and generating proteins list containing fileName and chain
        self.proteinList = []
        # New dictionary for lexical code for specific chain only
        self.newDictForLexicalCode = {} 
        # dictionary for storing seq and chain identity only
        self.seqchainIdentity = {}

    def thetaClass(self, theta):
        return thetaClass(theta)

    def dist12Class(self, dist12):
        return dist12Class(dist12)
    
    # Calculating the distance between the amino acids 
    def calDistance(self, l1_index, l2_index):
        x1 = self.xCoordinate[l1_index]
        x2 = self.xCoordinate[l2_index]
        y1 = self.yCoordinate[l1_index]
        y2 = self.yCoordinate[l2_index]
        z1 = self.zCoordinate[l1_index]
        z2 = self.zCoordinate[l2_index]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) **2 + (z2 - z1) **2)

    def findTheIndex(self, l2_index, p1, q1, r1):
        if l2_index == p1:
            l1_index0 = q1
            l2_index1 = r1
        elif l2_index == q1:
            l1_index0 = p1
            l2_index1 = r1
        elif l2_index == r1:
            l1_index0 = p1
            l2_index1 = q1
        return l1_index0, l2_index1
    
    def readDrugLexicalCsv(self, csvFile):
        df = pd.read_csv(csvFile)
        self.aminoAcidLabelWithCode = dict(zip(df['atom'], df['seq']))
        self.aminoAcidLabelWithCode.update(dict(zip(df['ATOM'], df['seq'])))

    def readSeqAndIdentityChain(self, data_dir, fileName, chain):
        with open(f'{data_dir}{fileName.upper()}.pdb', 'r') as pdbFile:
            for line in pdbFile:
                # Do not take CA if the peptide bond is broken i.e after the TER
                if ((line[0:6].rstrip()=="ENDMDL") or (line[0:6].rstrip()=='TER'and line[21].rstrip()==chain)):
                    break
                if (line[0:6].rstrip()=="MODEL" and int(line[10:14].rstrip())>1):
                    break                       
                if (line.startswith("ATOM") and line[21:22].strip()==chain) and not line[16:20].strip().startswith('B'):
                    # In this section I am taking the residue type as SER even it is ASER (note)
                    self.seqchainIdentity[line[22:27].strip()] = line[17:20].strip()
        
    # This function is used to extract alpha carbons and then calculate theta and key
    def calcuTheteAndKey(self, data_dir, fileName, chain, seq_value, chain_identity, output_subdir, output_option='both', mirror_image=False):
        # Resetting lists for each protein calculation
        self.totalKeys = []
        self.maxDistList = []
        self.keyFreq = {}
        incrementVal=0
        self.newDictForLexicalCode = {}
        self.aminoAcidCode = {}
        self.aminoSeqNum = {}
        with open(f'{data_dir}{fileName.upper()}.pdb', 'r') as pdbFile:
            for line in pdbFile:
                try: 
                    # Do not take CA if the peptide bond is broken i.e after the TER
                    if ((line[0:6].rstrip()=="ENDMDL") or (line[0:6].rstrip()=='TER'and line[21].rstrip()==chain)):
                        break
                    if (line[0:6].rstrip()=="MODEL" and int(line[10:14].rstrip())>1):
                        break                       
                    if (line.startswith("ATOM") and line[21:22].strip()==chain and line[22:27].strip() == seq_value and line[17:20].strip() == chain_identity and not line[16:20].strip().startswith('B') and line[77:80].strip() != "H" and line[77:80].strip() != "D"):
                        # Reading the lines in pdb file and then assigning residue (VAL) to its value (20)
                        self.aminoAcidCode[incrementVal]=int(self.aminoAcidLabelWithCode[line[13:16].rstrip()])
                        # This is the sequence number of the amino acid stored (Residue seq number)
                        self.aminoSeqNum[incrementVal]=str(line[22:27])
                        self.xCoordinate[incrementVal]=(float(line[30:38]))
                        self.yCoordinate[incrementVal]=(float(line[38:46]))
                        self.zCoordinate[incrementVal]=(float(line[46:54]))
                        self.newDictForLexicalCode[line[13:16].rstrip()] = int(self.aminoAcidLabelWithCode[line[13:16].rstrip()])
                        incrementVal+=1
                except Exception as e:
                    print("Their is an error in: ", line, pdbFile)
                    print(e)

        if ((chain_identity == "GLY" and len(self.aminoAcidCode) == 4) or (chain_identity == "ALA" and len(self.aminoAcidCode) == 5) or (chain_identity == "VAL" and len(self.aminoAcidCode) == 7) or (chain_identity == "LEU" and len(self.aminoAcidCode) == 8) or 
            (chain_identity == "ILE" and len(self.aminoAcidCode) == 8) or (chain_identity == "PRO" and len(self.aminoAcidCode) == 7) or (chain_identity == "PHE" and len(self.aminoAcidCode) == 11) or (chain_identity == "TYR" and len(self.aminoAcidCode) == 12) or 
            (chain_identity == "TRP" and len(self.aminoAcidCode) == 14) or (chain_identity == "SER" and len(self.aminoAcidCode) == 6) or (chain_identity == "THR" and len(self.aminoAcidCode) == 7) or (chain_identity == "MET" and len(self.aminoAcidCode) == 8) or 
            (chain_identity == "CYS" and len(self.aminoAcidCode) == 6) or (chain_identity == "HIS" and len(self.aminoAcidCode) == 10) or (chain_identity == "LYS" and len(self.aminoAcidCode) == 9) or (chain_identity == "ARG" and len(self.aminoAcidCode) == 11) or 
            (chain_identity == "ASP" and len(self.aminoAcidCode) == 8) or (chain_identity == "GLU" and len(self.aminoAcidCode) == 9) or (chain_identity == "ASN" and len(self.aminoAcidCode) == 8) or (chain_identity == "GLN" and len(self.aminoAcidCode) == 9) or
            (chain_identity == "TPO" and len(self.aminoAcidCode) == 11) or (chain_identity == "SEP" and len(self.aminoAcidCode) == 10) or (chain_identity == "PTR" and len(self.aminoAcidCode) == 16)):
            tripletsFile = open(f"{data_dir}{output_subdir}/{fileName}_{chain}_{seq_value}_{chain_identity}.keys_theta29_dist18", "w") if output_option in ['both', 'triplets'] else None
            keyFreqFile = open(f"{data_dir}{output_subdir}/{fileName}_{chain}_{seq_value}_{chain_identity}.keys_Freq_theta29_dist18", "w") if output_option in ['both', 'keys'] else None
            for i in range(0, len(self.aminoAcidCode) - 2):
                for j in range(i+1, len(self.aminoAcidCode) - 1):
                    for k in range(j+1, len(self.aminoAcidCode)):
                        # This is a dictionary to keep the index and the labels
                        labelIndexToUse={}
                        # First, Second and Third label and Index
                        labelIndexToUse[self.aminoAcidCode[i]]=i
                        labelIndexToUse[self.aminoAcidCode[j]]=j
                        labelIndexToUse[self.aminoAcidCode[k]]=k
                        # First, Second and Third amino label list
                        self.initAminoLabel[0]=self.aminoAcidCode[i]
                        self.initAminoLabel[1]=self.aminoAcidCode[j]
                        self.initAminoLabel[2]=self.aminoAcidCode[k]
                        # Sorted labels from above list 
                        sortedAminoLabel=list(self.initAminoLabel)
                        # Reverse order from above sorted list
                        sortedAminoLabel.sort(reverse=True)

                        # The fourth case when l1=l2=l3
                        if (sortedAminoLabel[0] == sortedAminoLabel[1]) and (sortedAminoLabel[1]==sortedAminoLabel[2]):
                            distance1_2 = self.calDistance(i,j)
                            distance1_3 = self.calDistance(i,k)
                            distance2_3 = self.calDistance(j,k)
                            if distance1_2 >= (max(distance1_2,distance1_3,distance2_3)):
                                l1_index0=i
                                l2_index1=j
                                l3_index2=k
                            elif distance1_3 >= (max(distance1_2,distance1_3,distance2_3)):
                                l1_index0=i
                                l2_index1=k
                                l3_index2=j
                            else:
                                l1_index0=j
                                l2_index1=k
                                l3_index2=i

                        # Third condition when l1=l2>l3
                        elif(sortedAminoLabel[0]==sortedAminoLabel[1])and(sortedAminoLabel[1]!=sortedAminoLabel[2]):
                            l3_index2 = labelIndexToUse[sortedAminoLabel[2]]
                            indices = self.findTheIndex(l3_index2,i,j,k)
                            first = l3_index2
                            second = indices[0]
                            third  =indices[1]
                            distance1_3=self.calDistance(second,first)
                            distance2_3=self.calDistance(third,first)
                            if distance1_3>=distance2_3:
                                l1_index0=indices[0]
                                l2_index1=indices[1]	
                            else:
                                l1_index0=indices[1]
                                l2_index1=indices[0]

                        # Second condition when l1>l2=l3     
                        elif(sortedAminoLabel[0]!=sortedAminoLabel[1])and(sortedAminoLabel[1]==sortedAminoLabel[2]):
                            l1_index0=labelIndexToUse[sortedAminoLabel[0]]
                            indices = self.findTheIndex(l1_index0,i,j,k)
                            if self.calDistance(l1_index0,indices[0])>= self.calDistance(l1_index0,indices[1]):
                                l2_index1=indices[0]
                                l3_index2=indices[1]	
                            else:
                                l3_index2=indices[0]
                                l2_index1=indices[1]

                        # First condition when l1!=l2!=l3
                        elif(sortedAminoLabel[0]!=sortedAminoLabel[1])and(sortedAminoLabel[0]!=sortedAminoLabel[2])and(sortedAminoLabel[1]!=sortedAminoLabel[2]):
                            # Getting the index from the labelIndexToUse from sortedAminoLabel use
                            for index in range(0,3):
                                self.sortedAminoIndex[index]=labelIndexToUse[sortedAminoLabel[index]]
                            l1_index0=self.sortedAminoIndex[0]
                            l2_index1=self.sortedAminoIndex[1]
                            l3_index2=self.sortedAminoIndex[2]

                        distance01=self.calDistance(l1_index0,l2_index1)
                        # Calculating the mid distance
                        midDis01 = distance01/2
                        distance02=self.calDistance(l1_index0,l3_index2)
                        distance12=self.calDistance(l2_index1,l3_index2)
                        # Calculating the max distance (D)
                        maxDistance=max(distance01,distance02,distance12)
                        # Calculating the mid point 
                        m1 = (self.xCoordinate[l1_index0]+ self.xCoordinate[l2_index1])/2
                        m2 = (self.yCoordinate[l1_index0]+ self.yCoordinate[l2_index1])/2
                        m3 = (self.zCoordinate[l1_index0]+ self.zCoordinate[l2_index1])/2

                        # Calculating the d3 distance
                        d3 = math.sqrt((m1 - self.xCoordinate[l3_index2])**2+(m2 - self.yCoordinate[l3_index2])**2+(m3 - self.zCoordinate[l3_index2])**2)

                        # Calculating thetaAngle1
                        thetaAngle1 = 180*(math.acos((distance02**2-midDis01**2-d3**2)/(2*midDis01*d3)))/3.14

                        # Check in which category does the angle falls
                        if thetaAngle1<=90:
                            theta = thetaAngle1
                        else:
                            theta = abs(180-thetaAngle1)

                        # Calculating the bin values for theta and max distance
                        binTheta = self.thetaClass(theta)
                        binLength = self.dist12Class(maxDistance)
                        
                        aminoAcidR1 = list(self.newDictForLexicalCode.keys())[l1_index0]
                        aminoAcidR2 = list(self.newDictForLexicalCode.keys())[l2_index1]
                        aminoAcidR3 = list(self.newDictForLexicalCode.keys())[l3_index2]

                        # These are the sequence number of the three amino acids
                        seqNumber1 = list(self.aminoSeqNum.values())[l1_index0]
                        seqNumber2 = list(self.aminoSeqNum.values())[l2_index1]
                        seqNumber3 = list(self.aminoSeqNum.values())[l3_index2]

                        # These are the coordinates of the three amino acids
                        aminoAcidC10, aminoAcidC11, aminoAcidC12 = self.xCoordinate[l1_index0], self.yCoordinate[l1_index0], self.zCoordinate[l1_index0]
                        aminoAcidC20, aminoAcidC21, aminoAcidC22 = self.xCoordinate[l2_index1], self.yCoordinate[l2_index1], self.zCoordinate[l2_index1]
                        aminoAcidC30, aminoAcidC31, aminoAcidC32 = self.xCoordinate[l3_index2], self.yCoordinate[l3_index2], self.zCoordinate[l3_index2]

                        # Calculating the triplets key value
                        tripletKeys = self.dLen*self.dtheta*(self.numOfLabels**2)*(self.aminoAcidCode[l1_index0]-1)+self.dLen*self.dtheta*(self.numOfLabels)*(self.aminoAcidCode[l2_index1]-1)+self.dLen*self.dtheta*(self.aminoAcidCode[l3_index2]-1)+self.dtheta*(binLength-1)+(binTheta-1)

                        # Its just the negation of the keys
                        if mirror_image and thetaAngle1 > 90:
                            tripletKeys = (-1) * tripletKeys

                        # Filtering out the distinct keys
                        if tripletKeys in self.keyFreq:
                            self.keyFreq[tripletKeys]+=1
                        else:
                            self.keyFreq[tripletKeys] = 1

                        # These are the info of all the triplets
                        if output_option in ['both', 'triplets'] and tripletsFile:
                            tripletInfoAll = (str(tripletKeys)+"\t"+str(aminoAcidR1)+"\t"+str(seqNumber1)+"\t"+str(aminoAcidR2)+"\t"+str(seqNumber2)+"\t"+str(aminoAcidR3)+"\t"+str(seqNumber3)+"\t"+str(binTheta)+"\t"+str(theta)+"\t"+str(binLength)+"\t"+str(maxDistance)+"\t"+str(aminoAcidC10)+"\t"+str(aminoAcidC11)+"\t"+str(aminoAcidC12)+"\t"+str(aminoAcidC20)+"\t"+str(aminoAcidC21)+"\t"+str(aminoAcidC22)+"\t"+str(aminoAcidC30)+"\t"+str(aminoAcidC31)+"\t"+str(aminoAcidC32)+"\n")
                            tripletsFile.writelines(tripletInfoAll)

            if output_option in ['both', 'keys'] and keyFreqFile:
                # Storing the distinct keys in a file
                for values in self.keyFreq:
                    keyFreqFile.writelines([str(values), '\t', str(self.keyFreq[values]), "\n"]) 
            # Close the files
            if keyFreqFile:
                keyFreqFile.close()
            if tripletsFile:
                tripletsFile.close()
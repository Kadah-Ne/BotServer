from discord.ext import commands
from discord.utils import get
import re
import random
import discord
import math

class CogFunStuff(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.listCitations = self.getCitations()
        
    def rollDie(self,dice:int) :
        return random.randint(1,dice)
    
    def splitCommande(self,input):
        outputs = {}
        trimmed = input.replace(" ","")
        listDies = trimmed.split("&")
        for die in listDies :
            
            mod = -1
            occ = -1
            opp = ""
            kh = -1
            kl = -1
            splitD = re.split("d",die,flags=re.IGNORECASE)
            sides_mods = splitD[-1].lower()
    
            if "kh" in sides_mods:
                sides_mods,kh = sides_mods.split("kh")
            elif 'kl' in sides_mods :
                sides_mods,kl = sides_mods.split("kl")
            occ = splitD[0]

            if sides_mods.__contains__('+'):
                sides = sides_mods.split("+")[0]
                mod = sides_mods.split("+")[-1]
                opp = "+"
            elif sides_mods.__contains__('-'):
                sides = sides_mods.split("-")[0]
                mod = sides_mods.split("-")[-1]
                opp = "-"
            else : 
                sides = re.split("-",sides_mods,flags=re.IGNORECASE)[0]
            outputs[die] = self.rollMyDie(mod,occ,opp,sides,kh,kl)
        return(outputs)
                
    
    def rollMyDie(self,mod,occ,item,sides,kh,kl) :
        numlist = []           
        sides = int(sides)
        if sides >= 2000:
            raise Exception("Fuckyou")

        if mod != -1:
            mod = int(mod)                       
        number = 0
        if occ == "":
            occ = 1
        else:
            occ = int(occ)
        if occ < 1 or occ >=1000 :
            raise Exception("Fuck You")
        for i in range (occ):
            rand = self.rollDie(sides)
            numlist.append(rand)
            number += rand
        if item == "+":
            number += mod
        elif item == "-" :
            number -= mod

        if occ == 1 :
            
            textchain = str(numlist[0])
            return [number,textchain]
        else : 
            numlist.sort()
            textchain = ""
            if (kh == -1 and kl == -1) or (len(numlist) < int(kh) or len(numlist) < int(kl)) :
                for i in numlist: 
                    textchain += f"+{i}"
                
                textchain = textchain[1:]
                
                if len(textchain) > 1500:
                    return [number]
                else :
                    return [number,textchain]
            else :
                kh = int(kh)
                kl = int(kl)
                if kh > -1 :
                    newList = numlist[-1*int(kh):]
                else :
                    newList = numlist[:int(kl)]
                for i in newList: 
                        textchain += f"+{i}"
                number = sum(newList)
                textchain = textchain[1:]
                return [number,textchain]
        

    @commands.command (name="roll", aliases = ["Roll","rolls","Rolls","r","R"])
    async def roll(self,ctx,* die : str):
        die = ''.join([str(ele) + '' for ele in die])
        try :
            outputs = self.splitCommande(die)
            finalTxt = "Summary of your roll :\n"
            for die in outputs :
                mod = ""
                
                if len(re.findall(r'\+\d*',die)) > 0 :
                    mod = re.findall(r'\+\d*',die)[0]
                if len(outputs[die]) == 2 :              
                    finalTxt += f"{outputs[die][0]} : {outputs[die][1]}{mod} on the {die}\n"
                else : 
                    finalTxt += f"{outputs[die][0]}{mod} on the {die}\n"
            await ctx.channel.send(finalTxt)
            
        except :
            await ctx.channel.send("Utilisez le format [x]D[y]+/-[z][kh/kl][w]<&[x]D[y]+/-[z][kh/kl][w]> pour la commande ou x,y,z,w sont des nombres entiers")


    @commands.command(name="inspiration", aliases = ["inspi","Inspiration","Inspi"])
    async def inspiration(self,ctx):
        listQuotes = ["Shoot for the moon! Even if you miss, you'll... something... something... stars!","You know who you remind me of? Me!","You've got a great personality!","You're doing pretty well!","You must be great -- you're hanging out with me!","You're not the ugliest person I've ever met!","NEVER limit yourself!","Hey... player...! You're really good at this game!","It's in our moments of decision that destiny is shaped!","You're -- uh -- special?","Follow your hearts... and stuff.","Don't belive in yourself, believe in me because I believe in you!","It's Cute That You All Think You're The Heroes Of This Little Adventure, But, You're Not.","I Just Bought A Pony Made Of Diamonds Because I'm Rich.","These Pretzels Suck!","Vault Hunter Looks For The New Vault. Vault Hunter Gets Killed. By Me. Seeing The Problem Here?","This Guy Rushes Me With A Spoon... A Freakin' Spoon!","Stop Shooting Yourself, Stop Shooting Yourself!!","Never Meet Your heroes, Kid, They're All Dicks. Every Last One.","Jimmy, Please Make A Note: I'm Strangling Mister Moorin For Bringing Up My Wife.","Too many people die.’ Give me a break. That’s what people DO!"]
        choiceCitations = random.choice(await self.getCitations())
        if(random.randint(1,100) > 95 ):
            await ctx.channel.send(f"{random.choice(listQuotes)}")
        else:
            await ctx.channel.send(f"{choiceCitations}")
        if(random.randint(1,100) > 95 ):
            await ctx.channel.send(f"https://i.ytimg.com/vi/PjNsUrr497c/maxresdefault.jpg")
        else:
            await ctx.channel.send(f"https://tenor.com/view/borderlands-inspired-skill-borderlands-inspired-gif-20917083")

    async def getCitations(self):
        channelId = 772904165189222410
        channel = self.bot.get_channel(channelId)
        guild = channel.guild
        msgs = [msg async for msg in channel.history(oldest_first=False)]
        listCita = []
        for i in msgs:
            # if i.content.__contains__("@"):
            #     cited = i.content.split(">")[0].split("@")[1]
            #     member = guild.get_member(cited).name
            #     contenue = userCited + " " +i.content.split(">")[1]
            # else :
            #     contenue = i.content
            contenue = i.content
            if(i.attachments != []):
                contenue+= f" {i.attachments[0]}"
            listCita.append(contenue)
        return listCita

            

        
    
        
local imagestring = 
local imagewidth =  --max size 248
local imageheight =  --max size 168

snes9x.speedmode("turbo")

local cursorx = 0x7e0226
local cursory = 0x7e0227
local cursortype = 0x7E0426 -- 86 stamp, 84 color picker

local leftbound = 2 
local topbound = 24  
local rightbound = 250        
local bottombound = 192       

local stepsize = 1

local colorList2={'1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'}
local colorTotals={}
local colorList={}

for i=1,15 do
   colorTotals[i] = {0,colorList2[i]}
   for w in string.gfind(imagestring, colorList2[i]) do
       colorTotals[i][1] = colorTotals[i][1] + 1
   end
end

table.sort(colorTotals, function(a,b) return a[1]<b[1] end) --use < for small to large, > for large to small

colorList = colorTotals

--for centering images that do not match the aspect ratio
leftbound = math.floor(leftbound + (rightbound-imagewidth-leftbound)/2)
topbound = math.floor(topbound + (bottombound-imageheight-topbound)/2)
local colorSelected = '-'

local function paintdot(dotx,doty)
      local targetx = (dotx * stepsize) + leftbound
      local targety = (doty * stepsize) + topbound
      local currentx = memory.readbyte(cursorx)
      local currenty = memory.readbyte(cursory)
      
      while math.abs(currentx-targetx)>5 or math.abs(currenty-targety)>5 do
            if currentx < targetx then
               joypad.set(1,{right=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currentx > targetx then
               joypad.set(1,{left=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currenty < targety or memory.readbyte(cursortype)==84 then
               joypad.set(1,{down=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currenty > targety and memory.readbyte(cursortype)~=84 then
               joypad.set(1,{up=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            currentx = memory.readbyte(cursorx)
            currenty = memory.readbyte(cursory)
      end
      
      while currentx ~= targetx or currenty ~= targety do
            if currentx < targetx then
               joypad.set(1,{right=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currentx > targetx then
               joypad.set(1,{left=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currenty < targety or memory.readbyte(cursortype)==84 then
               joypad.set(1,{down=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currenty > targety and memory.readbyte(cursortype)~=84 then
               joypad.set(1,{up=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            currentx = memory.readbyte(cursorx)
            currenty = memory.readbyte(cursory)
      end
      joypad.set(1,{X=1})
      snes9x.frameadvance()
end

local function chooseColor(thecolor)
      local targetx
      local targety = 14
      if(thecolor=='1') then
           targetx = 30
      end
      if(thecolor=='2') then
           targetx = 44
      end
      if(thecolor=='3') then
           targetx = 58
      end
      if(thecolor=='4') then
           targetx = 72
      end
      if(thecolor=='5') then
           targetx = 86
      end
      if(thecolor=='6') then
           targetx = 100
      end
      if(thecolor=='7') then
           targetx = 114
      end
      if(thecolor=='8') then
           targetx = 128
      end
      if(thecolor=='9') then
           targetx = 142
      end
      if(thecolor=='A') then
           targetx = 156
      end
      if(thecolor=='B') then
           targetx = 170
      end
      if(thecolor=='C') then
           targetx = 184
      end
      if(thecolor=='D') then
           targetx = 198
      end
      if(thecolor=='E') then
           targetx = 212
      end
      if(thecolor=='F') then
           targetx = 226
      end

      local currentx = memory.readbyte(cursorx)
      local currenty = memory.readbyte(cursory)

      while math.abs(currentx-targetx)>5 or math.abs(currenty-targety)>5 do
            if currentx < targetx then
               joypad.set(1,{right=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currentx > targetx then
               joypad.set(1,{left=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currenty < targety  then
               joypad.set(1,{down=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currenty > targety  then
               joypad.set(1,{up=1,L=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            currentx = memory.readbyte(cursorx)
            currenty = memory.readbyte(cursory)
      end

      while currentx ~= targetx or currenty ~= targety or memory.readbyte(cursortype)==86 do
            if currentx < targetx then
               joypad.set(1,{right=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currentx > targetx then
               joypad.set(1,{left=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            if currenty > targety or memory.readbyte(cursortype)==86 then
               joypad.set(1,{up=1})
               snes9x.frameadvance()
               snes9x.frameadvance()
               snes9x.frameadvance()
            end
            currentx = memory.readbyte(cursorx)
            currenty = memory.readbyte(cursory)
      end
      joypad.set(1,{X=1})
      snes9x.frameadvance()
      joypad.set(1,{X=1})
      snes9x.frameadvance()
      joypad.set(1,{X=1})
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()
      snes9x.frameadvance()

      colorSelected = thecolor
end

local thisposition = 1

for k = 1,15 do
   snes9x.message(colorTotals[k][2])
   chooseColor(colorTotals[k][2])

   for i = 0,imageheight-1 do
       for j = 0,imagewidth-1 do
               thisposition = i*imagewidth + j + 1

               curPix = string.sub(imagestring,thisposition,thisposition)

               if curPix == colorTotals[k][2] then
                  paintdot(j,i)
               end
       end
   end
end

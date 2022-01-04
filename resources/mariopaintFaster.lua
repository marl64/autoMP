local imagestring = 
local imagewidth =  -- Max 248px
local imageheight =  -- Max 168px

-- Original script by alden, modified for autoMP by marl

snes9x.speedmode("turbo")

-- Cursor memory addresses
local cursorx = 0x7e0226
local cursory = 0x7e0227
local cursortype = 0x7E0426 -- 86 - stamp, 84 - color picker

-- Bounding area for the cursor. Not super precise but it works
local leftbound = 2 
local topbound = 24  
local rightbound = 250        
local bottombound = 192       

-- Useful coordinates
local stampchange = {240,13}
local stampchange2 = {240,10}
local arrow = {234,210}
local fillselect = {160,210}
local centre = {128,104}
local stampselect = {100,210}

local stepsize = 1
local thisposition = 1
local colorSelected = '-'

local colorList2 = {'1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'}
local colorTotals = {}
local colorList = {}

for i = 1, 15 do
   colorTotals[i] = {0, colorList2[i]}
   for w in string.gfind(imagestring, colorList2[i]) do
      colorTotals[i][1] = colorTotals[i][1] + 1
   end
end

table.sort(colorTotals, function(a,b) return a[1] < b[1] end) -- Use < for small to large, > for large to small

colorList = colorTotals
colorMost = colorTotals[15][2]
-- For centering images that do not match the aspect ratio
leftbound = math.floor(leftbound + (rightbound-imagewidth-leftbound)/2)
topbound = math.floor(topbound + (bottombound-imageheight-topbound)/2)
rightbound = leftbound + imagewidth
bottombound = topbound + imageheight

local function setjoy(buttons,frames)
   joypad.set(1,buttons)
   for i=1,frames do
      snes9x.frameadvance()
   end
end

local function moveto(position)
   local targetx = position[1]
   local targety = position[2]

   local currentx = memory.readbyte(cursorx)
   local currenty = memory.readbyte(cursory)

   while math.abs(currentx-targetx)>5 or math.abs(currenty-targety)>5 do
      if currentx < targetx then
         setjoy({right=1,L=1},3)
      end
      if currentx > targetx then
         setjoy({left=1,L=1},3)
      end
      if currenty < targety then
         setjoy({down=1,L=1},3)
      end
      if currenty > targety then
         setjoy({up=1,L=1},3)
      end
      currentx = memory.readbyte(cursorx)
      currenty = memory.readbyte(cursory)
   end

   while currentx ~= targetx or currenty ~= targety do
      if currentx < targetx then
         setjoy({right=1},3)
      end
      if currentx > targetx then
         setjoy({left=1},3)
      end
      if currenty < targety then
         setjoy({down=1},3)
      end
      if currenty > targety then
         setjoy({up=1},3)
      end
      currentx = memory.readbyte(cursorx)
      currenty = memory.readbyte(cursory)
   end
   setjoy({X=1},3)
end


local function paintdot(dotx,doty)
   local targetx = (dotx * stepsize) + leftbound
   local targety = (doty * stepsize) + topbound
   local currentx = memory.readbyte(cursorx)
   local currenty = memory.readbyte(cursory)
   
   while math.abs(currentx-targetx)>5 or math.abs(currenty-targety)>5 do
      if currentx < targetx then
         setjoy({right=1,L=1},3)
      end
      if currentx > targetx then
         setjoy({left=1,L=1},3)
      end
      if currenty < targety or memory.readbyte(cursortype)==84 then
         setjoy({down=1,L=1},3)
      end
      if currenty > targety and memory.readbyte(cursortype)~=84 then
         setjoy({up=1,L=1},3)
      end
      currentx = memory.readbyte(cursorx)
      currenty = memory.readbyte(cursory)
   end
   
   while currentx ~= targetx or currenty ~= targety do
      if currentx < targetx then
         setjoy({right=1},3)
      end
      if currentx > targetx then
         setjoy({left=1},3)
      end
      if currenty < targety or memory.readbyte(cursortype)==84 then
         setjoy({down=1},3)
      end
      if currenty > targety and memory.readbyte(cursortype)~=84 then
         setjoy({up=1},3)
      end
      currentx = memory.readbyte(cursorx)
      currenty = memory.readbyte(cursory)
   end
   setjoy({X=3},3)
end

local function chooseColor(thecolor)
   local colorcheck = {
      ['1']=30,
      ['2']=44,
      ['3']=58,
      ['4']=72,
      ['5']=86,
      ['6']=100,
      ['7']=114,
      ['8']=128,
      ['9']=142,
      ['A']=156,
      ['B']=170,
      ['C']=184,
      ['D']=198,
      ['E']=212,
      ['F']=226,
   }

   local targetx = colorcheck[thecolor]
   local targety = 14

   local currentx = memory.readbyte(cursorx)
   local currenty = memory.readbyte(cursory)

   while math.abs(currentx-targetx)>5 or math.abs(currenty-targety)>5 do
      if currentx < targetx then
         setjoy({right=1,L=1},3)
      end
      if currentx > targetx then
         setjoy({left=1,L=1},3)
      end
      if currenty < targety or memory.readbyte(cursortype)==84 then
         setjoy({down=1,L=1},3)
      end
      if currenty > targety and memory.readbyte(cursortype)~=84 then
         setjoy({up=1,L=1},3)
      end
      currentx = memory.readbyte(cursorx)
      currenty = memory.readbyte(cursory)
   end

   while currentx ~= targetx or currenty ~= targety or memory.readbyte(cursortype)==86 do
      if currentx < targetx then
         setjoy({right=1},3)
      end
      if currentx > targetx then
         setjoy({left=1},3)
      end
      if currenty > targety or memory.readbyte(cursortype)==86 then
         setjoy({up=1},3)
      end
      currentx = memory.readbyte(cursorx)
      currenty = memory.readbyte(cursory)
   end
   setjoy({X=1},1)
   setjoy({X=1},1)
   setjoy({X=1},12)
   colorSelected = thecolor
end

local function fillcolor(Most)
   moveto(stampchange2)
   chooseColor(Most)
   moveto(arrow)
   moveto(fillselect)
   moveto(centre)
   --wait somehow
   moveto(stampselect)
   moveto(arrow)
   moveto(stampchange2)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
   setjoy({X=1},3)
end
local numcolors=15

if imageheight<168 and imagewidth<248 then
   chooseColor(colorMost)
   for j=0,imagewidth-1 do
      paintdot(j,0)
   end
   for j=0,imageheight-1 do
      paintdot(imagewidth-1,j)
   end
   for j=imagewidth-1,0,-1 do
      paintdot(j,imageheight-1)
   end
   for j=imageheight-1,0,-1 do
      paintdot(0,j)
   end
   fillcolor(colorMost)
   numcolors=14

elseif imageheight<168 and imagewidth==248 then
   chooseColor(colorMost)
   for j=0,248 do
      paintdot(j,0)
   end
   for j=248,0,-1 do
      paintdot(j,imageheight-1)
   end
   fillcolor(colorMost)
   numcolors=14

elseif imageheight==168 and imagewidth<248 then
   chooseColor(colorMost)
   for j=0,168 do
      paintdot(0,j)
   end
   for j=168,0,-1 do
      paintdot(imagewidth-1,j)
   end
   fillcolor(colorMost)
   numcolors=14

elseif imagewidth==248 and imageheight==168 then
   fillcolor(colorMost)
   numcolors=14

end

for k = 1,numcolors do
   -- snes9x.message(colorTotals[k][2])
   chooseColor(colorTotals[k][2])

   for i = 0,imageheight-1 do

      if math.fmod(i+1,2) == 0 then -- boustrophedon :))))
         for j = imagewidth-1,0,-1 do
            thisposition = i*imagewidth + j + 1

            curPix = string.sub(imagestring,thisposition,thisposition)

            if curPix == colorTotals[k][2] then
               paintdot(j,i)
            end
         end

      else
         for j = 0,imagewidth-1 do
            thisposition = i*imagewidth + j + 1

            curPix = string.sub(imagestring,thisposition,thisposition)

            if curPix == colorTotals[k][2] then
               paintdot(j,i)
            end
         end
      end
   end
end
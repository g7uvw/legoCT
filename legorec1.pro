function readgreyjpeg, filename
  read_jpeg, filename+'.jpeg', image
  dims = size(image, /dimensions)
  image = reform(rebin(image, 1, dims[1], dims[2]))
  return, image
end

function get_projection, filename
  common data, dark, light
  proj = readgreyjpeg(filename)*1.0
  proj -= dark
  proj /= light
  p = where(proj le 0, count)
  if count gt 0 then proj(p) = 0.1
  proj = -alog(proj)
  return, proj
end 
  

common data, dark, light
dark = readgreyjpeg("dark")
light = readgreyjpeg("light")
light -= dark
close,1
openw, 1, 'test.con'
for a = 0, 200 do begin
  filename = string(a, format='projection_%03d')
  proj = get_projection(filename)
  writeu, 1, proj
endfor
close,1
end

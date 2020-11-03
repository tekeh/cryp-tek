using Polynomials
using StatsBase

function ckks_naive_encode(x)
	# Encodes vector as a complex-coefficient polynomial ring
	dim = length(x) ## number of elements
	root_unity = exp(1*π*im/(dim)) 	
	vec = [root_unity^(2*k-1) for k in 1:dim]
	vd = vandermonde(vec)
	coeffs = inv(vd) * x
	poly = Polynomial(coeffs)
end

function ckks_naive_decode(p::Polynomial{Complex{Float64}})
	# Decodes a polynomial into a vector
	order = length(p)-1 ## order of polnomial
	root_unity = exp(1*π*im/(order+1) ) 	
	vec = [p(root_unity^(2*k-1)) for k in 1:order+1]
end

function vandermonde(x)
	# Calculates the vandermonde matrix given vector (of evaluation positions) 
	dim = length(x)
	vd = [ xi^k for xi=x, k=0:dim-1] 
end

function pi_transform(x)
	# Projects complex vector to a vector of half the size
	N = div(length(x),2)
	x[1:N]
end

function pi_inverse(x)
	# Expands complex vector with its complex conjugate
	vcat(x, conj(reverse(x)))
end

function poly_basis_coeffs(x, prec=100)
	dim = length(x) ## number of elements
	root_unity = exp(1*π*im/(dim)) 	
	vec = [root_unity^(2*k-1) for k in 1:dim]
	b_basis = vandermonde(vec)

	# Project complex number unto this basis
	coeffs  = [ real(dot(vd[:,k], x))/norm(vd[:,k])^2 for k=1:size(vd)[2] ]
	#int_coords = coordinate_wise_random_rounding(coeffs)
	#y = b_basis * int_coords
	#p = ckks_naive_encode(y)
end

function ckks_encode(x, scale=64)
##	dim = length(x) ## number of elements
#	root_unity = exp(1*π*im/(dim)) 	
#	vec = [root_unity^(2*k-1) for k in 1:dim]
#	b_basis = vandermonde(vec)
#	 
	scaled_pi_x = pi_inverse(x) * scale
	rounded_scaled_pi_x = cwrr_project(scaled_pi_x)
	p = ckks_naive_encode(rounded_scaled_pi_x)
	# Round coeffs after the fact
	poly_coeffs = [round(c) for c in p.coeffs]
	p_round = Polynomial(poly_coeffs)
end

function ckks_decode(p::Polynomial, scale=64)
	rescaled_p = p/scale
	x = ckks_naive_decode(rescaled_p)
	pi_x = pi_transform(x)
end



function round_coordinates(coords)
	[c - floor(c) for c in coords]
end

function coordinate_wise_random_rounding(coords)
	# Rounds coordinates randomly
	r = round_coordinates(coords)
	dir = [sample([c, c-1], aweights([1-c,c])) for c in r]

	rounded_coord = coords - dir
	rounded_coord = [round(coord) for coord in rounded_coord]
end

function cwrr_project(x)
	# Projects vector onto lattice using coordinate wise random rounding
	coeffs = poly_basis_coeffs(x) 
	rounded_coords = coordinate_wise_random_rounding(coeffs)
	lattice_point = vd * rounded_coords
end



# Checks
coords = [1, 1, 1, 1]
dim=4
root_unity = exp(1*π*im/(dim)) 	
vec = [root_unity^(2*k-1) for k in 1:dim]
vd = vandermonde(vec)

b = vd * coords
p = ckks_naive_encode(b)
println(p)

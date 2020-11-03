using Polynomials
using StatsBase
using LinearAlgebra

struct CKKS
	vector_dim::Int64
	scale::Float64
	xi::Complex{Float64}
end
CKKS(x) = CKKS(x, 1.0, exp(1*pi*im/x))
CKKS(vec) = CKKS(length(vec), 1.0, exp(1*pi*im/length(vec)))
CKKS(vec, scale) = CKKS(length(vec), scale, exp(1*pi*im/length(vec)))

## Vandermonde Matrix definitions
function vandermonde(x)
	# Calculates the vandermonde matrix given vector (of evaluation positions) 
	dim = length(x)
	vd = [ xi^k for xi=x, k=0:dim-1] 
end

function vandermonde(xi::Complex{Float64}, dim)
	vd = [xi^((2*k-1)*(l-1)) for k=1:dim, l=1:dim]
end

## Encoding/Decoding functions
function ckks_canon_encode(x)
	# Encodes vector as a complex-coefficient polynomial ring. Also called sigma inv
	dim = length(x) ## number of elements
	root_unity = exp(1*π*im/(dim)) 	
	vec = [root_unity^(2*k-1) for k in 1:dim]
	vd = vandermonde(vec)
	coeffs = inv(vd) * x
	poly = Polynomial(coeffs)
end

function ckks_canon_decode(p::Polynomial{Complex{Float64}})
	# Decodes a polynomial into a vector. Also called the "sigma" transform
	order = length(p)-1 ## order of polnomial
	root_unity = exp(1*π*im/(order+1) ) 	
	vec = [p(root_unity^(2*k-1)) for k in 1:order+1]
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
	vd = vandermonde(vec) # columns make up b basis

	# Project complex number unto this basis
	coeffs  = [ real(dot(vd[:,k], x))/norm(vd[:,k])^2 for k=1:size(vd)[2] ]
end

function ckks_encode(x, scale=64)
	scaled_pi_x = pi_inverse(x) * scale
	rounded_scaled_pi_x = cwrr_project(scaled_pi_x)
	p = ckks_canon_encode(rounded_scaled_pi_x)
	# Round coeffs after the fact
	poly_coeffs = [round(c) for c in p.coeffs]
	p_round = Polynomial(poly_coeffs)
end

function ckks_decode(p::Polynomial, scale=64)
	rescaled_p = p/scale
	x = ckks_canon_decode(rescaled_p)
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
	dim = length(x) ## number of elements
	root_unity = exp(1*π*im/(dim)) 	
	vec = [root_unity^(2*k-1) for k in 1:dim]
	vd = vandermonde(vec) # columns make up b basis
	# Projects vector onto lattice using coordinate wise random rounding
	coeffs = poly_basis_coeffs(x) 
	rounded_coords = coordinate_wise_random_rounding(coeffs)
	lattice_point = vd * rounded_coords
end

# Checks

vec = [1+5im, 2-6.3im, 2.71 + 3.14im]
CKKS(vec)
p = ckks_encode(vec)
reconstructed_vec = ckks_decode(p)

using Polynomials

function ckks_encode(x)
	# Encodes vector as a complex-coefficient polynomial ring
	dim = length(x) ## number of elements
	root_unity = exp(1*π*im/(dim)) 	
	vec = [root_unity^(2*k-1) for k in 1:dim]
	vd = vandermonde(vec)
	coeffs = inv(vd) * x
	poly = Polynomial(coeffs)
end

function ckks_decode(p::Polynomial{Complex{Float64}})
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

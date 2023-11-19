### A Pluto.jl notebook ###
# v0.19.32

using Markdown
using InteractiveUtils

# This Pluto notebook uses @bind for interactivity. When running this notebook outside of Pluto, the following 'mock version' of @bind gives bound variables a default value (instead of an error).
macro bind(def, element)
    quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ f40eaade-8684-11ee-314f-417d56196857
using ColorTypes, Colors, PlutoUI, ColorVectorSpace, ColorSchemes

# ╔═╡ a2cc7815-0a50-4feb-9f26-aade2062dce0
md"""
See the original post at [oklab](https://bottosson.github.io/posts/oklab/).

The minimum lightness for RGB is at L=0.12
"""

# ╔═╡ 7a3fba0c-181d-47ee-8464-9a6fe6a5b10c
"`Oklch` is the Luminance-Chroma-Hue, Polar-Oklab colorspace."
struct Oklch{T<:AbstractFloat} <: Color{T,3}
    l::T # Lightness in [0,1]
    c::T # Chroma
    h::T # Hue in [0,360]
end

# ╔═╡ 00651e12-0d21-4e4b-975c-439bb13c1b60
begin
	
function Base.convert(::Type{RGB}, c::Oklch) 
	L = c.l
	a = c.c * cos(deg2rad(c.h))
	b = c.c * sin(deg2rad(c.h))

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_^3
    m = m_^3
    s = s_^3

    
	r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
	g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
	b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
	return RGB(r, g, b)
end

function Base.convert(::Type{ColorTypes.RGB24}, c::Oklch{Float64})
	crgb = convert(RGB, c)
	return convert(RGB24, crgb)
end


function Base.convert(::Type{Oklch}, c::RGB) 
    l = 0.4122214708 * c.r + 0.5363325363 * c.g + 0.0514459929 * c.b
	m = 0.2119034982 * c.r + 0.6806995451 * c.g + 0.1073969566 * c.b
	s = 0.0883024619 * c.r + 0.2817188376 * c.g + 0.6299787005 * c.b

    l_ = l^(1/3)
    m_ = m^(1/3)
    s_ = s^(1/3)

 
    L = 0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_
	a = 1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_
    b = 0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_
	c = sqrt(a^2 + b^2)
	h = rad2deg(atan(b, a))

	return Oklch(L, c, h)
end
end

# ╔═╡ cdf89b85-397d-4dcc-92c1-2985f56ec0da
md"""
lightness:  $(@bind l Slider(0:0.01:1))
chroma: $(@bind c Slider(0:0.002:0.2))
hue: $(@bind h Slider(0:0.1:360))
"""

# ╔═╡ 98f1f812-2872-44ab-a646-2dca8c1a96d6
md"""
lightness:  $(@bind l2 Slider(0:0.01:1))
chroma: $(@bind c2 Slider(0:0.002:0.2))
hue: $(@bind h2 Slider(0:0.1:360))
"""

# ╔═╡ d74e23c2-721d-43d5-b9f4-a76074025fd5
md"""
lightness:  $(@bind l4 Slider(0:0.01:1))
chroma: $(@bind c4 Slider(0:0.002:0.2))
hue: $(@bind h4 Slider(0:0.1:360))
"""

# ╔═╡ f071ca1f-6759-4d11-b7b6-356c94697432
[convert(RGB, Oklch(l4, 0., 0.)), RGB(0., 0., 0.)]

# ╔═╡ 1e58b487-7481-43d9-9d07-b546bad8db55
md"""
colour1: lightness = $(l)
chroma = $(c)
hue = $(h)

colour2: lightness = $(l2)
chroma = $(c2)
hue = $(h2)
"""

# ╔═╡ 7ecb9cea-6bed-4a5c-91b2-0fb2e44e05e7
function is_valid(c::RGB)
	for sym in [:r, :b, :g]
		val = getfield(c, sym)
		if val < 0 || val > 1
			return false
		end
	end
	return true
end

# ╔═╡ 8172f11b-a0dc-4728-be59-27a609e7aeae
begin
	function mean_rgb(colour::RGB)
		if !is_valid(colour)
			return RGB(1., 0., 0.)
		end
		return colour
	end

	mean_rgb(colour::Oklch) = mean_rgb(convert(RGB, colour))
	safe_rgb(colour::Oklch) = safe_rgb(convert(RGB, colour))

	is_valid(c::Oklch) = is_valid(convert(RGB, c))
end

# ╔═╡ 0a06be11-8fbd-4390-a4d7-633ac05419ad
begin
	okcolour1 = Oklch(l, c, h)
	okcolour2 = Oklch(l2, c2, h2)
	is_valid.(convert.(RGB, [okcolour1, okcolour2]))
end

# ╔═╡ 7f22eebb-ba27-49c4-92ca-51729f2591ea
mean_rgb.([okcolour1, RGB(0., 0., 0.), okcolour2, RGB(1., 1., 1.)])

# ╔═╡ 7c7aef36-e0d7-461e-a5a4-28704e8c2601
function safe_rgb(colour::RGB)
	c2 = copy(colour)
	if !is_valid(colour)
		for sym in [:r, :b, :g]
			val = getfield(c2, sym)
			val = max(val, 0)
			val = min(val, 1)
			setfield!(c2, sym) = val
		end
	end
	return c2
end

# ╔═╡ b1aacbbf-8458-47f8-9413-868d393d189d
function huerange(c1::Oklch, c2::Oklch, N::Int; increasing::Bool=true)
	if  increasing
		if c1.h > c2.h
			dh = c2.h + 360 - c1.h
		else
			dh = c2.h - c1.h
		end
	else
		if c1.h < c2.h
			dh = c2.h + 360 - c1.h
		else
			dh = c2.h - c1.h
		end
	end
	
	dl = (c2.l - c1.l)
	dc = c2.c - c1.c

	out = Oklch[]
	for i in 1:N
		x = i/N
		l = c1.l + x*dl
		h = mod(c1.h + dh*x, 360.)
		c = c1.c + x*dc
		colour = Oklch(l, c, h)
		push!(out, colour)
	end
	
	return out
end

# ╔═╡ e8b0d805-72d8-419d-84fb-c64b5d628fd8
begin
	N = 256
	cblack = Oklch(0.12, c, h)
	cwhite = Oklch(1., 0., h2)

	cmap1 = mean_rgb.(huerange(okcolour1, okcolour2, N, increasing=true))
	cmap2 = mean_rgb.(huerange(Oklch(l4, c4, h), okcolour2, N, increasing=true))
	cmap3 = mean_rgb.(huerange(okcolour1, cwhite, N, increasing=false))
	cmap4 = mean_rgb.(huerange(Oklch(0.12, 0., 0.), cwhite, N, increasing=false))
end;

# ╔═╡ e3c86b41-17f4-4303-9fe8-706bb17e33df
cmap1

# ╔═╡ 25038572-cbbd-45f7-ae79-ea977b974181
cmap3

# ╔═╡ 98e36933-5746-46d2-a505-58c9e3d3cb86
cmap2

# ╔═╡ 79742909-8403-45e1-9207-2aaf8e114562
cmap4

# ╔═╡ 4c048143-f8f4-4bbf-84e9-9933d03d7af0
md"""
lightness:  $(@bind l3 Slider(0:0.01:1))
chroma: $(@bind c3 Slider(0:0.002:0.2))
hue: $(@bind h3 Slider(0:0.1:360))
"""

# ╔═╡ 56059071-7a1f-47a2-8e2e-33e9f8ab224e
mean_rgb.(huerange(Oklch(0.2, c3, h3), Oklch(1., c3, h3), 256, increasing=false))

# ╔═╡ 7c0427e2-cf14-41f3-a209-5dd3339b47c5
begin
	function max_lightness(lightness, chroma, hue)
		colours = huerange(Oklch(lightness, chroma, hue), Oklch(1., chroma, hue), 1_000)
		mask = is_valid.(colours)
		colours = colours[mask]
		if length(colours) < 1
			return 0
		end
		return maximum([col.l for col in colours])
	end

	function lightest_hue(lightness, chroma)
		hues = 0:0.01:360
		mls = max_lightness.(lightness, chroma, hues)
		idx = argmax(mls)
		return hues[idx]
	end
end

# ╔═╡ 8e1f9d9b-b868-4d3b-bdc0-c978973687e7
lightest_hue(0., 0.05)

# ╔═╡ c51481b2-ee7c-42b1-a3ee-6fbd8239b71f
begin
	function min_lightness(lightness, chroma, hue)
		colours = huerange(Oklch(lightness, chroma, hue), Oklch(1., chroma, hue), 1_000)
		mask = is_valid.(colours)
		colours = colours[mask]
		if length(colours) < 1
			return 0
		end
		return minimum([col.l for col in colours])
	end
	function darkest_hue(lightness, chroma)
		hues = 0:0.01:360
		mls = min_lightness.(lightness, chroma, hues)
		idx = argmin(mls)
		return hues[idx]
	end
end

# ╔═╡ c3dda1a7-1249-4e9d-b0c4-a7cb8eafcac4
darkest_hue(0.1, 0.1)

# ╔═╡ 76dd0b78-c17f-446b-a82c-3743e44cabda
@bind colour_in ColorPicker()

# ╔═╡ 128efa13-0d75-4fc6-a1b6-5a886ac6a9b7
print(convert(Oklch, colour_in))

# ╔═╡ f8b7aef0-c04f-424d-b49f-52a12d2335f8
col1 = convert(Oklch, colour_in);

# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
ColorSchemes = "35d6a980-a343-548e-a6ea-1d62b119f2f4"
ColorTypes = "3da002f7-5984-5a60-b8a6-cbb66c0b333f"
ColorVectorSpace = "c3611d14-8923-5661-9e6a-0046d554d3a4"
Colors = "5ae59095-9a9b-59fe-a467-6f913c188581"
PlutoUI = "7f904dfe-b85e-4ff6-b463-dae2292396a8"

[compat]
ColorSchemes = "~3.24.0"
ColorTypes = "~0.11.4"
ColorVectorSpace = "~0.10.0"
Colors = "~0.12.10"
PlutoUI = "~0.7.53"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

julia_version = "1.9.3"
manifest_format = "2.0"
project_hash = "f87dbdb25c5c3299d255bf0da8680b443d43e0d5"

[[deps.AbstractPlutoDingetjes]]
deps = ["Pkg"]
git-tree-sha1 = "91bd53c39b9cbfb5ef4b015e8b582d344532bd0a"
uuid = "6e696c72-6542-2067-7265-42206c756150"
version = "1.2.0"

[[deps.ArgTools]]
uuid = "0dad84c5-d112-42e6-8d28-ef12dabb789f"
version = "1.1.1"

[[deps.Artifacts]]
uuid = "56f22d72-fd6d-98f1-02f0-08ddc0907c33"

[[deps.Base64]]
uuid = "2a0f44e3-6c83-55bd-87e4-b1978d98bd5f"

[[deps.ColorSchemes]]
deps = ["ColorTypes", "ColorVectorSpace", "Colors", "FixedPointNumbers", "PrecompileTools", "Random"]
git-tree-sha1 = "67c1f244b991cad9b0aa4b7540fb758c2488b129"
uuid = "35d6a980-a343-548e-a6ea-1d62b119f2f4"
version = "3.24.0"

[[deps.ColorTypes]]
deps = ["FixedPointNumbers", "Random"]
git-tree-sha1 = "eb7f0f8307f71fac7c606984ea5fb2817275d6e4"
uuid = "3da002f7-5984-5a60-b8a6-cbb66c0b333f"
version = "0.11.4"

[[deps.ColorVectorSpace]]
deps = ["ColorTypes", "FixedPointNumbers", "LinearAlgebra", "Requires", "Statistics", "TensorCore"]
git-tree-sha1 = "a1f44953f2382ebb937d60dafbe2deea4bd23249"
uuid = "c3611d14-8923-5661-9e6a-0046d554d3a4"
version = "0.10.0"

    [deps.ColorVectorSpace.extensions]
    SpecialFunctionsExt = "SpecialFunctions"

    [deps.ColorVectorSpace.weakdeps]
    SpecialFunctions = "276daf66-3868-5448-9aa4-cd146d93841b"

[[deps.Colors]]
deps = ["ColorTypes", "FixedPointNumbers", "Reexport"]
git-tree-sha1 = "fc08e5930ee9a4e03f84bfb5211cb54e7769758a"
uuid = "5ae59095-9a9b-59fe-a467-6f913c188581"
version = "0.12.10"

[[deps.CompilerSupportLibraries_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "e66e0078-7015-5450-92f7-15fbd957f2ae"
version = "1.0.5+0"

[[deps.Dates]]
deps = ["Printf"]
uuid = "ade2ca70-3891-5945-98fb-dc099432e06a"

[[deps.Downloads]]
deps = ["ArgTools", "FileWatching", "LibCURL", "NetworkOptions"]
uuid = "f43a241f-c20a-4ad4-852c-f6b1247861c6"
version = "1.6.0"

[[deps.FileWatching]]
uuid = "7b1f6079-737a-58dc-b8bc-7a2ca5c1b5ee"

[[deps.FixedPointNumbers]]
deps = ["Statistics"]
git-tree-sha1 = "335bfdceacc84c5cdf16aadc768aa5ddfc5383cc"
uuid = "53c48c17-4a7d-5ca2-90c5-79b7896eea93"
version = "0.8.4"

[[deps.Hyperscript]]
deps = ["Test"]
git-tree-sha1 = "8d511d5b81240fc8e6802386302675bdf47737b9"
uuid = "47d2ed2b-36de-50cf-bf87-49c2cf4b8b91"
version = "0.0.4"

[[deps.HypertextLiteral]]
deps = ["Tricks"]
git-tree-sha1 = "7134810b1afce04bbc1045ca1985fbe81ce17653"
uuid = "ac1192a8-f4b3-4bfe-ba22-af5b92cd3ab2"
version = "0.9.5"

[[deps.IOCapture]]
deps = ["Logging", "Random"]
git-tree-sha1 = "d75853a0bdbfb1ac815478bacd89cd27b550ace6"
uuid = "b5f81e59-6552-4d32-b1f0-c071b021bf89"
version = "0.2.3"

[[deps.InteractiveUtils]]
deps = ["Markdown"]
uuid = "b77e0a4c-d291-57a0-90e8-8db25a27a240"

[[deps.JSON]]
deps = ["Dates", "Mmap", "Parsers", "Unicode"]
git-tree-sha1 = "31e996f0a15c7b280ba9f76636b3ff9e2ae58c9a"
uuid = "682c06a0-de6a-54ab-a142-c8b1cf79cde6"
version = "0.21.4"

[[deps.LibCURL]]
deps = ["LibCURL_jll", "MozillaCACerts_jll"]
uuid = "b27032c2-a3e7-50c8-80cd-2d36dbcbfd21"
version = "0.6.3"

[[deps.LibCURL_jll]]
deps = ["Artifacts", "LibSSH2_jll", "Libdl", "MbedTLS_jll", "Zlib_jll", "nghttp2_jll"]
uuid = "deac9b47-8bc7-5906-a0fe-35ac56dc84c0"
version = "7.84.0+0"

[[deps.LibGit2]]
deps = ["Base64", "NetworkOptions", "Printf", "SHA"]
uuid = "76f85450-5226-5b5a-8eaa-529ad045b433"

[[deps.LibSSH2_jll]]
deps = ["Artifacts", "Libdl", "MbedTLS_jll"]
uuid = "29816b5a-b9ab-546f-933c-edad1886dfa8"
version = "1.10.2+0"

[[deps.Libdl]]
uuid = "8f399da3-3557-5675-b5ff-fb832c97cbdb"

[[deps.LinearAlgebra]]
deps = ["Libdl", "OpenBLAS_jll", "libblastrampoline_jll"]
uuid = "37e2e46d-f89d-539d-b4ee-838fcccc9c8e"

[[deps.Logging]]
uuid = "56ddb016-857b-54e1-b83d-db4d58db5568"

[[deps.MIMEs]]
git-tree-sha1 = "65f28ad4b594aebe22157d6fac869786a255b7eb"
uuid = "6c6e2e6c-3030-632d-7369-2d6c69616d65"
version = "0.1.4"

[[deps.Markdown]]
deps = ["Base64"]
uuid = "d6f4376e-aef5-505a-96c1-9c027394607a"

[[deps.MbedTLS_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "c8ffd9c3-330d-5841-b78e-0817d7145fa1"
version = "2.28.2+0"

[[deps.Mmap]]
uuid = "a63ad114-7e13-5084-954f-fe012c677804"

[[deps.MozillaCACerts_jll]]
uuid = "14a3606d-f60d-562e-9121-12d972cd8159"
version = "2022.10.11"

[[deps.NetworkOptions]]
uuid = "ca575930-c2e3-43a9-ace4-1e988b2c1908"
version = "1.2.0"

[[deps.OpenBLAS_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "Libdl"]
uuid = "4536629a-c528-5b80-bd46-f80d51c5b363"
version = "0.3.21+4"

[[deps.Parsers]]
deps = ["Dates", "PrecompileTools", "UUIDs"]
git-tree-sha1 = "a935806434c9d4c506ba941871b327b96d41f2bf"
uuid = "69de0a69-1ddd-5017-9359-2bf0b02dc9f0"
version = "2.8.0"

[[deps.Pkg]]
deps = ["Artifacts", "Dates", "Downloads", "FileWatching", "LibGit2", "Libdl", "Logging", "Markdown", "Printf", "REPL", "Random", "SHA", "Serialization", "TOML", "Tar", "UUIDs", "p7zip_jll"]
uuid = "44cfe95a-1eb2-52ea-b672-e2afdf69b78f"
version = "1.9.2"

[[deps.PlutoUI]]
deps = ["AbstractPlutoDingetjes", "Base64", "ColorTypes", "Dates", "FixedPointNumbers", "Hyperscript", "HypertextLiteral", "IOCapture", "InteractiveUtils", "JSON", "Logging", "MIMEs", "Markdown", "Random", "Reexport", "URIs", "UUIDs"]
git-tree-sha1 = "db8ec28846dbf846228a32de5a6912c63e2052e3"
uuid = "7f904dfe-b85e-4ff6-b463-dae2292396a8"
version = "0.7.53"

[[deps.PrecompileTools]]
deps = ["Preferences"]
git-tree-sha1 = "03b4c25b43cb84cee5c90aa9b5ea0a78fd848d2f"
uuid = "aea7be01-6a6a-4083-8856-8a6e6704d82a"
version = "1.2.0"

[[deps.Preferences]]
deps = ["TOML"]
git-tree-sha1 = "00805cd429dcb4870060ff49ef443486c262e38e"
uuid = "21216c6a-2e73-6563-6e65-726566657250"
version = "1.4.1"

[[deps.Printf]]
deps = ["Unicode"]
uuid = "de0858da-6303-5e67-8744-51eddeeeb8d7"

[[deps.REPL]]
deps = ["InteractiveUtils", "Markdown", "Sockets", "Unicode"]
uuid = "3fa0cd96-eef1-5676-8a61-b3b8758bbffb"

[[deps.Random]]
deps = ["SHA", "Serialization"]
uuid = "9a3f8284-a2c9-5f02-9a11-845980a1fd5c"

[[deps.Reexport]]
git-tree-sha1 = "45e428421666073eab6f2da5c9d310d99bb12f9b"
uuid = "189a3867-3050-52da-a836-e630ba90ab69"
version = "1.2.2"

[[deps.Requires]]
deps = ["UUIDs"]
git-tree-sha1 = "838a3a4188e2ded87a4f9f184b4b0d78a1e91cb7"
uuid = "ae029012-a4dd-5104-9daa-d747884805df"
version = "1.3.0"

[[deps.SHA]]
uuid = "ea8e919c-243c-51af-8825-aaa63cd721ce"
version = "0.7.0"

[[deps.Serialization]]
uuid = "9e88b42a-f829-5b0c-bbe9-9e923198166b"

[[deps.Sockets]]
uuid = "6462fe0b-24de-5631-8697-dd941f90decc"

[[deps.SparseArrays]]
deps = ["Libdl", "LinearAlgebra", "Random", "Serialization", "SuiteSparse_jll"]
uuid = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"

[[deps.Statistics]]
deps = ["LinearAlgebra", "SparseArrays"]
uuid = "10745b16-79ce-11e8-11f9-7d13ad32a3b2"
version = "1.9.0"

[[deps.SuiteSparse_jll]]
deps = ["Artifacts", "Libdl", "Pkg", "libblastrampoline_jll"]
uuid = "bea87d4a-7f5b-5778-9afe-8cc45184846c"
version = "5.10.1+6"

[[deps.TOML]]
deps = ["Dates"]
uuid = "fa267f1f-6049-4f14-aa54-33bafae1ed76"
version = "1.0.3"

[[deps.Tar]]
deps = ["ArgTools", "SHA"]
uuid = "a4e569a6-e804-4fa4-b0f3-eef7a1d5b13e"
version = "1.10.0"

[[deps.TensorCore]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "1feb45f88d133a655e001435632f019a9a1bcdb6"
uuid = "62fd8b95-f654-4bbd-a8a5-9c27f68ccd50"
version = "0.1.1"

[[deps.Test]]
deps = ["InteractiveUtils", "Logging", "Random", "Serialization"]
uuid = "8dfed614-e22c-5e08-85e1-65c5234f0b40"

[[deps.Tricks]]
git-tree-sha1 = "eae1bb484cd63b36999ee58be2de6c178105112f"
uuid = "410a4b4d-49e4-4fbc-ab6d-cb71b17b3775"
version = "0.1.8"

[[deps.URIs]]
git-tree-sha1 = "67db6cc7b3821e19ebe75791a9dd19c9b1188f2b"
uuid = "5c2747f8-b7ea-4ff2-ba2e-563bfd36b1d4"
version = "1.5.1"

[[deps.UUIDs]]
deps = ["Random", "SHA"]
uuid = "cf7118a7-6976-5b1a-9a39-7adc72f591a4"

[[deps.Unicode]]
uuid = "4ec0a83e-493e-50e2-b9ac-8f72acf5a8f5"

[[deps.Zlib_jll]]
deps = ["Libdl"]
uuid = "83775a58-1f1d-513f-b197-d71354ab007a"
version = "1.2.13+0"

[[deps.libblastrampoline_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "8e850b90-86db-534c-a0d3-1478176c7d93"
version = "5.8.0+0"

[[deps.nghttp2_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "8e850ede-7688-5339-a07c-302acd2aaf8d"
version = "1.48.0+0"

[[deps.p7zip_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "3f19e933-33d8-53b3-aaab-bd5110c3b7a0"
version = "17.4.0+0"
"""

# ╔═╡ Cell order:
# ╠═a2cc7815-0a50-4feb-9f26-aade2062dce0
# ╠═f40eaade-8684-11ee-314f-417d56196857
# ╟─7a3fba0c-181d-47ee-8464-9a6fe6a5b10c
# ╟─00651e12-0d21-4e4b-975c-439bb13c1b60
# ╠═7f22eebb-ba27-49c4-92ca-51729f2591ea
# ╟─cdf89b85-397d-4dcc-92c1-2985f56ec0da
# ╠═98f1f812-2872-44ab-a646-2dca8c1a96d6
# ╟─d74e23c2-721d-43d5-b9f4-a76074025fd5
# ╠═f071ca1f-6759-4d11-b7b6-356c94697432
# ╟─1e58b487-7481-43d9-9d07-b546bad8db55
# ╟─0a06be11-8fbd-4390-a4d7-633ac05419ad
# ╠═e8b0d805-72d8-419d-84fb-c64b5d628fd8
# ╠═e3c86b41-17f4-4303-9fe8-706bb17e33df
# ╠═25038572-cbbd-45f7-ae79-ea977b974181
# ╠═98e36933-5746-46d2-a505-58c9e3d3cb86
# ╠═79742909-8403-45e1-9207-2aaf8e114562
# ╠═7ecb9cea-6bed-4a5c-91b2-0fb2e44e05e7
# ╠═8172f11b-a0dc-4728-be59-27a609e7aeae
# ╠═7c7aef36-e0d7-461e-a5a4-28704e8c2601
# ╠═b1aacbbf-8458-47f8-9413-868d393d189d
# ╟─4c048143-f8f4-4bbf-84e9-9933d03d7af0
# ╠═56059071-7a1f-47a2-8e2e-33e9f8ab224e
# ╠═8e1f9d9b-b868-4d3b-bdc0-c978973687e7
# ╠═c3dda1a7-1249-4e9d-b0c4-a7cb8eafcac4
# ╠═7c0427e2-cf14-41f3-a209-5dd3339b47c5
# ╠═c51481b2-ee7c-42b1-a3ee-6fbd8239b71f
# ╠═76dd0b78-c17f-446b-a82c-3743e44cabda
# ╠═128efa13-0d75-4fc6-a1b6-5a886ac6a9b7
# ╠═f8b7aef0-c04f-424d-b49f-52a12d2335f8
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002

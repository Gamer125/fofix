uniform float time;
uniform vec4 fretcol;
uniform bool fail;

varying vec4 col;
varying vec4 failcol;
varying vec3 pos;

void main()
{
	float alphafog = 7.0-gl_Vertex.z;
	col = fretcol;
	col.a *= alphafog;
	failcol.rgb=vec3(1.0,0.0,0.0);
	if (fail) failcol.a=0.2*max(sin(time*10),0.0)*alphafog;
	else failcol.a=0.0;
	gl_Position = ftransform();
	pos=gl_Position.xyz;
} 
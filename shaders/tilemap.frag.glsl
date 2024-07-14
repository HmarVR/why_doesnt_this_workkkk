#version 300 es
precision highp float;
precision highp int;
precision highp sampler2D;
precision highp sampler2DArray;

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 fragPos;
in vec4 instance_pos_data;

uniform sampler2DArray Tiles;
uniform sampler2DArray Decor;

#include "uniforms"


void main() {
	int ArrayIndex = int(instance_pos_data.z);
	bool bol = ArrayIndex<decor;
	
	vec3 color = bol ? texture(Tiles, vec3(uv_0, ArrayIndex)).rgb : texture(Decor, vec3(uv_0, ArrayIndex-decor)).rgb;

	if (color==vec3(0)) {
		discard;
	}
	fragColor = vec4(color, 1);
}
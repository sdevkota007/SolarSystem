#version 130
in vec3 position;
in vec2 inTexCoords;
in vec3 vertNormal;

//uniform mat4 transform;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;
uniform mat3 normalMatrix;

out vec2 newTexture;
out vec3 fragNormal;
out vec3 fragPosition;

void main()
{
    fragNormal = normalize(normalMatrix * normalize(vertNormal));
    gl_Position = projection * view * model * vec4(position, 1.0f);

    fragPosition = (view * model * vec4(position, 1.0f)).xyz;
    newTexture = inTexCoords;
}
#version 130
in vec2 newTexture;
in vec3 fragNormal;
in vec3 fragPosition;

uniform mat3 normalMatrix;
uniform mat4 view;

uniform vec4 Global_ambient;
uniform vec4 Light_ambient;
uniform vec4 Light_diffuse;
uniform vec4 Light_specular;
uniform vec3 Light_location;
uniform vec4 Material_ambient;
uniform vec4 Material_diffuse;
uniform vec4 Material_specular;
uniform float Material_shininess;

uniform sampler2D samplerTexture;


out vec4 outColor;



void main()
{
    //vec3 LightDir = normalize(normalMatrix * Light_location);

    vec3 lightPositionInViewSpace = (view * (vec4(Light_location, 1.0f))).xyz;
    vec3 LightDir = normalize((lightPositionInViewSpace - fragPosition));

    // get the half light between the light ray and the viewpoint
    vec3 view_dir = normalize(- fragPosition);
    vec3 Light_half = normalize(LightDir + view_dir);

    float n_dot_pos = max(0.0, dot(fragNormal, LightDir));


    //for blinn-phong model
    float n_dot_half = 0.0;
    if (n_dot_pos > -.05) {
        n_dot_half = pow(max(0.0,dot(Light_half, fragNormal)), Material_shininess);
    }

    //for phong model
    //float n_dot_view = pow(max(0.0,dot( view_vec, fragNormal)), Material_shininess);

    vec3 lightIntensity = vec3(clamp(
    (
        (Global_ambient * Material_ambient)
        + (Light_ambient * Material_ambient)
        + (Light_diffuse * Material_diffuse * n_dot_pos)
        + (Light_specular * Material_specular * n_dot_half)
    ), 0.0, 1.0));

    vec4 texel = texture(samplerTexture, newTexture);
    outColor = vec4(texel.rgb * lightIntensity, texel.a);
}
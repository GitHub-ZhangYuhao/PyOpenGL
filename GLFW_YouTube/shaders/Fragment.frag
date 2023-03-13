# version 330

in vec3 v_color;
in vec2 uv;
uniform sampler2D Texture0;

out vec4 out_color;

void main()
{
    vec4 TexData = texture(Texture0 , uv);

    out_color = vec4(TexData.xyz, 1.0);
}
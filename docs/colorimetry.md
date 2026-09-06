# Colorimetría y estilo

## Cómo se mide

1. **Piel**: mediana CIELAB de la máscara de piel derivada de la malla (sin ojos, cejas ni labios), descartando el 15 % más oscuro y el 10 % más claro (sombras y brillos).
2. **Pelo**: mediana LAB de la máscara `hair` de SegFormer, si cubre más de 400 píxeles.
3. **Iris**: disco central de cada iris (landmarks 468–477), sin la pupila (30 % más oscuro) ni el brillo (8 % más claro).
4. **Ejes**: subtono por ángulo de matiz de la piel (`atan2(b*, a*)`; frío < 49°, cálido > 61°, oliva con a* bajo), profundidad por L* de piel y pelo, croma por el croma del iris y el contraste pelo–piel, contraste por la mayor diferencia de L* entre piel, pelo y ojos.
5. **Estación**: cada una de las 12 tiene coordenadas en los tres ejes; se puntúa la cercanía y se devuelve el ranking con el margen entre la primera y la segunda.
6. **Forma de cara**: puntuación por índice facial, mandíbula/pómulos, anchura de mentón y sienes/pómulos.
7. **Camisas**: la máscara `cloth` de SegFormer se recolorea en LAB manteniendo L* relativa (pliegues y sombras) y sustituyendo a* y b* por los del color objetivo. 16 variantes en menos de un segundo.

Todo depende del balance de blancos y de la luz de la foto. El informe lo marca como orientativo y recomienda confirmarlo con una foto a luz de día.

## Las 12 estaciones

| id | Estación | Profundidad | Subtono | Croma | Metales | Resumen |
|---|---|---|---|---|---|---|
| `invierno_profundo` | Invierno profundo | deep | cool-neutral | clear | plata, platino, oro blanco | Pelo y ojos oscuros con piel de subtono frío o neutro. Aguanta el negro puro y los colores intensos y oscuros; los tonos polvorientos apagan. |
| `invierno_frio` | Invierno frío | medium | cool | clear | plata, platino | Subtono claramente frío con contraste alto entre pelo, piel y ojos. Colores puros, fríos y con contraste; nada cálido ni terroso. |
| `invierno_brillante` | Invierno brillante | medium | neutral-cool | bright | plata brillante, oro blanco | Ojos muy claros o brillantes frente a pelo oscuro: la característica dominante es la claridad. Colores saturados y limpios; los apagados y polvorientos restan. |
| `verano_claro` | Verano claro | light | cool-neutral | soft | plata mate, oro rosa claro | Conjunto claro y fresco: pelo rubio o castaño claro ceniza, piel clara, ojos claros. Tonos claros, suaves y fríos; el negro y los colores oscuros pesan. |
| `verano_frio` | Verano frío | medium | cool | soft | plata, oro blanco, perla | Subtono frío rosado con contraste medio. Colores fríos de intensidad media, suaves más que vivos; los cálidos amarillentos desentonan. |
| `verano_suave` | Verano suave | medium | neutral-cool | muted | plata mate, peltre, oro rosa mate | Conjunto de bajo contraste y colores apagados: castaño ceniza, ojos grises, verdes o avellana. Tonos velados y neutros; los colores muy puros y el negro dominan la cara. |
| `otono_suave` | Otoño suave | medium | neutral-warm | muted | oro mate, bronce, cobre envejecido | Bajo contraste con tirón cálido: castaño medio dorado, ojos avellana o verdes apagados. Tonos terrosos suaves y velados; los colores fríos y brillantes lavan. |
| `otono_calido` | Otoño cálido | medium | warm | medium | oro amarillo, cobre, latón | Subtono dorado o cobrizo inequívoco; pelo castaño rojizo, cobrizo o castaño dorado. Toda la gama tierra y especia; nada azulado ni rosa frío. |
| `otono_profundo` | Otoño profundo | deep | warm-neutral | medium | oro amarillo, bronce, cobre | Pelo y ojos oscuros con piel de subtono cálido o neutro-cálido. Colores oscuros, ricos y cálidos; aguanta bastante intensidad y el negro combinado con tierras. |
| `primavera_clara` | Primavera clara | light | warm-neutral | clear | oro claro, oro rosa | Conjunto claro y luminoso con tirón cálido: rubio dorado o castaño claro, piel clara con melocotón, ojos claros. Tonos claros, frescos y cálidos; nada oscuro ni pesado. |
| `primavera_calida` | Primavera cálida | medium | warm | clear | oro amarillo brillante | Subtono cálido dorado con colores claros y vivos: rubio dorado, cobrizo claro o castaño cálido, ojos claros o avellana dorada. Colores cálidos y limpios; evitar lo apagado y lo azulado. |
| `primavera_brillante` | Primavera brillante | medium | neutral-warm | bright | oro brillante, oro rosa | Alta claridad con tirón cálido: pelo oscuro o medio, ojos muy claros y luminosos. Colores vivos, saturados y ligeramente cálidos; lo polvoriento y apagado resta luz. |

## Formas de cara y cortes

| Forma | Criterio | Corte masculino | Corte femenino | Corte neutro | Monturas |
|---|---|---|---|---|---|
| Ovalada | Largo aproximadamente 1,4–1,6 veces el ancho; pómulos algo más anchos que mandíbula y frente; mentón redondeado. | Corte clásico con laterales cortos y volumen moderado arriba (side part o quiff bajo) | Media melena a los hombros con ondas suaves | Corte medio con textura y flequillo abierto | Casi cualquier montura; cuadradas o rectangulares añaden estructura |
| Redonda | Largo y ancho similares; pómulos anchos; mandíbula y mentón suaves sin ángulos. | Volumen y altura arriba con laterales muy cortos (pompadour o quiff alto) | Largo por debajo del hombro con capas que empiezan bajo la barbilla | Corte con altura arriba y laterales pegados | Monturas angulares rectangulares o cuadradas |
| Cuadrada | Mandíbula tan ancha como los pómulos y la frente; ángulos mandibulares marcados; mentón ancho. | Textura y movimiento arriba con laterales en degradado (no líneas rectas) | Capas largas y ondas sueltas que suavizan la mandíbula | Medio con capas y raya lateral | Redondas u ovaladas |
| Alargada | Largo claramente superior a 1,6 veces el ancho; frente, pómulos y mandíbula de anchura similar. | Laterales con algo de volumen y poca altura arriba | Flequillo recto o cortina (acorta) | Corte medio con volumen lateral | Monturas anchas y profundas (grandes) |
| Corazón | Frente y pómulos más anchos que la mandíbula; mentón estrecho o en punta. | Medio con volumen en la nuca y laterales medios | Bob o lob a la altura de la mandíbula con puntas hacia fuera (equilibra) | Corte con peso en la parte baja | Monturas más anchas abajo que arriba (aviador |
| Diamante | Pómulos claramente más anchos que frente y mandíbula; mentón estrecho. | Textura y flequillo hacia delante para ensanchar la frente | Flequillo cortina o lateral | Flequillo | Ovaladas |
| Triangular | Mandíbula más ancha que la frente y los pómulos. | Volumen y anchura arriba (quiff | Volumen en la coronilla y las sienes | Corte con peso arriba y ligero en la nuca | Monturas con detalle superior (browline |

## Palancas de expresión

Las variantes "más femenino" y "más masculino" de los looks y los cortes mueven estas palancas. No son juicios ni cambios de identidad: describen qué rasgos lee la mayoría como más femeninos o masculinos, según la literatura citada.

**feminine** · Mayor contraste facial (ojos y labios más oscuros que la piel), piel lisa y luminosa, cejas más altas y arqueadas, pelo con longitud o suavidad que enmarca la cara, líneas curvas en cuellos, monturas y accesorios.  
Fuentes: Russell 2009 Perception, Jones et al. 2015 Vision Research, Perrett 1998 Nature

**masculine** · Menor contraste facial, piel mate, cejas más rectas y bajas, mandíbula subrayada por barba o por líneas rectas, pelo corto con estructura, ángulos en cuellos, monturas y accesorios.  
Fuentes: Dixson & Brooks 2013 Evolution and Human Behavior, Russell 2009, Perrett 1998

**neutral** · Equilibrio entre las dos listas; textura y proporción por encima de códigos de género.  
Fuentes: Práctica de estilismo

## Reglas de contraste


- **high**: Combina claros y oscuros en el mismo conjunto (camisa blanca con chaqueta marino, negro con marfil). Los conjuntos monocromos medios apagan.
- **medium**: Un neutro más un color, o dos tonos con diferencia moderada. Evita el blanco óptico junto al negro puro cerca de la cara.
- **low**: Tonos sobre tonos y combinaciones suaves en la misma familia. El contraste fuerte (blanco/negro) domina la cara.

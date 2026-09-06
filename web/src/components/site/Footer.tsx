export function Footer({ extra }: { extra?: React.ReactNode }) {
  return (
    <footer className="mx-auto mt-24 max-w-[1240px] border-t border-line px-5 py-8 text-[12px] leading-relaxed text-muted-foreground md:px-7">
      <p className="max-w-[80ch]">facelab no presta servicios clínicos ni médicos. Las medidas son geométricas sobre una foto; los percentiles comparan con caras de tu grupo en un dataset público (MEBeauty), no con una norma clínica. Cualquier procedimiento o principio activo se consulta con un profesional. La asimetría leve es normal y no se corrige.</p>
      {extra}
    </footer>
  );
}

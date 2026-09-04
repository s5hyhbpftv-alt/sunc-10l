import { D } from './lib'

/* По-русски студия зовётся Настёна, но в латинской раскладке буквы «ё» нет.
   Ставим латинскую «ë» с диерезисом — точки садятся по метрикам шрифта — и
   красим её акцентом. Для химического класса две точки над знаком читаются
   ещё и как неподелённая электронная пара. */
export default function Studio({ className = 'studio' }) {
  const txt = D.texts['студия']
  const i = txt.toUpperCase().indexOf('NAST') + 4
  if (i < 4 || txt[i].toLowerCase() !== 'e') return <p className={className}>{txt}</p>
  const ё = txt[i] === txt[i].toUpperCase() ? 'Ë' : 'ë'
  return (
    <p className={className}>
      {txt.slice(0, i)}
      <span className="yo" title="здесь должна быть ё">{ё}</span>
      {txt.slice(i + 1)}
    </p>
  )
}

"""As oito situações de treino (seção 5.2 do desenho): número → (slug, título)."""

SITUACOES: dict[int, tuple[str, str]] = {
    1: ("imigracao", "Imigração no aeroporto ou na fronteira"),
    2: ("restaurante", "Restaurante: pedir, trocar algo, pedir a conta, gorjeta"),
    3: ("taxi", "Táxi ou carro de aplicativo"),
    4: ("policia", "Polícia: pedir ajuda e abordagem no trânsito"),
    5: ("conversa", "Puxar conversa sem ser inconveniente"),
    6: ("telefonar", "Telefonar para colegas e marcar reunião"),
    7: ("tecnologia", "Conversar sobre programação, IA e frameworks"),
    8: ("entrevista", "Entrevista de emprego para trabalho remoto"),
}

// Substitua a função de alocação no seu projeto por esta:
async function alocarPlantao(req, res) {
  const { medico_id, consultorio_id, data } = req.body;
  try {
    const novoPlantao = await db.query(
      `INSERT INTO plantoes (medico_id, consultorio_id, data) VALUES ($1, $2, $3) RETURNING *`,
      [medico_id, consultorio_id, data]
    );
    return res.status(201).json(novoPlantao.rows[0]);
  } catch (error) {
    if (error.code === '23505') {
      if (error.constraint === 'uk_medico_dia') {
        return res.status(409).json({ erro: "Este médico já possui plantão neste dia." });
      }
      if (error.constraint === 'uk_consultorio_dia') {
        return res.status(409).json({ erro: "Esta sala já está reservada neste dia." });
      }
    }
    return res.status(500).json({ erro: "Erro interno ao alocar." });
  }
}

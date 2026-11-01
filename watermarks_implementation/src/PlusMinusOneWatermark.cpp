#include "PlusMinusOneWatermark.h"

#include <fstream>
#include <iostream>

PlusMinusOneWatermark::PlusMinusOneWatermark(double detectThreshold, const std::vector<std::size_t> positions, std::vector<bool> reference, std::vector<bool> b) :
	Watermark(),
	m_detectThreshold(detectThreshold),
	m_positions(positions),
	m_reference(reference),
	m_b(b)
{
}

void PlusMinusOneWatermark::setDetectThreshold(double detectThreshold)
{
	m_detectThreshold = detectThreshold;
}

bool PlusMinusOneWatermark::embed(std::shared_ptr<VideoFrame> pframe, bool value)
{
	if (m_positions.size() != m_reference.size() || m_reference.size() != m_b.size())
		return false;

	if (!value && m_positions.empty())
		return true;

	//Embed `m_b` values at the `m_positions` with using `m_references` into pframe when `value` is true 
	//When `value`==false do nothing

	return true;
}

Watermark::DetectResult PlusMinusOneWatermark::detect(const std::shared_ptr<VideoFrame> pframe)
{
	if (m_positions.size() != m_reference.size() || m_reference.size() != m_b.size())
		return Watermark::DetectResult::FAILED;
	//extract embedded bits from the `m_positions` pixels using `m_reference` and compare extracting vector with m_b using `m_detectionThreshold` threshold (percentage of vectors similaryty)

}


std::vector<std::size_t> PlusMinusOneWatermark::createPositions(const std::shared_ptr<VideoFrame> &pframe, int count)
{
	if (count <= 0)
		return std::vector<std::size_t>();

	std::vector<std::size_t> positions;

	//generate random vector with count elements for received frame

	return positions;
}

std::vector<bool> PlusMinusOneWatermark::createReference(int count)
{
	if (count <= 0)
		return std::vector<bool>();

	std::vector<bool> reference;

	//generate random vector of embedded bits values

	return reference;
}

namespace
{
	void write_vector_bool (std::ofstream& file, const std::vector<bool>& vec) 
	{
		std::size_t size = vec.size();

		// Pack bits into bytes
		std::vector<unsigned char> bytes((size + 7) / 8, 0);
		for (std::size_t i = 0; i < size; ++i)
			if (vec[i]) bytes[i / 8] |= (1u << (i % 8));

		file.write(reinterpret_cast<const char*>(bytes.data()), bytes.size());
	}

	void read_vector_bool(std::size_t size, std::ifstream& file, std::vector<bool>& vec)
	{
		vec.assign(size, false);

		std::vector<unsigned char> bytes((size + 7) / 8);
		file.read(reinterpret_cast<char*>(bytes.data()), bytes.size());

		for (std::size_t i = 0; i < size; ++i)
			vec[i] = (bytes[i / 8] >> (i % 8)) & 1u;
	}
}

void PlusMinusOneWatermark::store(const std::vector<std::size_t>& positions, const std::vector<bool>& reference, const std::vector<bool>& b, const std::string& filename)
{
	std::ofstream file(filename, std::ios::binary);

	//store size to file
	
	//store vectors to file
	file.write(reinterpret_cast<const char*>(positions.data()), positions.size() * sizeof(std::size_t));
	write_vector_bool(file, reference);
	write_vector_bool(file, b);
}

bool PlusMinusOneWatermark::load(const std::string& filename, std::vector<std::size_t>& positions, std::vector<bool>& reference, std::vector<bool>& b)
{
	std::ifstream file(filename, std::ios::binary | std::ios::ate);
	if (!file) throw std::runtime_error("Cannot open file " + filename);

	//load size form 
	std::size_t size;

	positions.resize(size);
	reference.resize(size);
	b.resize(size);

	file.read(reinterpret_cast<char*>(positions.data()), size);
	read_vector_bool(size, file, reference);
	read_vector_bool(size, file, b);

	return true;
}

